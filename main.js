const { execSync } = require('child_process')
const express = require('express')
const bodyParser = require('body-parser')

async function fetch_and_update() {
  const BRANCH='master'
  const mirror_script = `
  set -x
  git fetch origin ${BRANCH}
  git reset --hard HEAD
  git checkout origin/${BRANCH}
  rm -rf _build
  sphinx-build -b html -d _build/doctrees . _build/html
  `
  try {
    await execSync(mirror_script, {stdio: 'inherit'})
  } catch (err) {
    console.error(err.toString())
  }
}

if (process.argv.length != 3) {
  console.error('Bad args.')
  process.exit()
}

const option = process.argv.pop()

if (option === 'serve') {
  /* setup webhook httpd */
  const app = express()
  app.use(bodyParser.json())
  app.use('/', express.static('./_build/html'))
  app.listen(8080)
  console.log('Webhook httpd ready.')

  process.on('SIGINT', function() {
    console.log('')
    console.log('Bye bye.')
    process.exit()
  })

  app.post('/webhook', async function (req, res) {
    const data = req.body
    const secret = process.env['WEBHOOKSECRET']
    console.log('[ request from ]', data.repository)

    if (data.secret === secret) {
      fetch_and_update()
      res.send('OK')
    } else {
      res.send('Wrong secret')
    }
  })

} else if (option === 'update') {
  /* run one-time script to manually update content */
  (async function () {
    await fetch_and_update()
    process.exit()
  })()

} else {
  console.error('Invalid arg option.')
}
