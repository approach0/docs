## Dependency

![](../static/dep.png)

(Boxes are external dependencies, circles are internal modules)

To generate this module dependency graph, issue commands below at the project top directory:

```sh
$ mkdir -p tmp
$ python3 proj-dep.py --targets > targets.mk
$ python3 proj-dep.py --dot > tmp/dep.dot
$ dot -Tpng tmp/dep.dot > tmp/dep.png
```
