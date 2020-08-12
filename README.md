<p align="center">
  <img src="docs/scriic.png" alt="Scriic" />
</p>

---

[![Documentation Status](https://readthedocs.org/projects/scriic/badge/?version=latest)](https://scriic.readthedocs.io/en/latest/?badge=latest)


**For installation instructions, getting started and the Scriic syntax
reference, see [ReadTheDocs](https://scriic.readthedocs.io/en/latest/).**


Scriic is a mini programming language for generating detailed (and more often
than not, overcomplicated) instructions. Here's an example program:

```
HOWTO Type <text"> using <keyboard>

char = LETTERS [text]
  SUB ./look.scriic
  PRM thing = [keyboard]
  GO

  key = DO Find the key on [keyboard] which displays [char"]

  SUB ./press_button.scriic
  PRM button = [key]
  GO
END
```

At the time of writing, this generates 110 steps to type "hello world"!
