Python API
**********

Running Files
=============

.. module:: scriic.run

To run a ``.scriic`` file, construct a :class:`FileRunner` with its file name.
This will immediately load metadata from the file, and a list of required
parameters is stored in :attr:`FileRunner.required_parameters`.

These parameters' values should be defined in a dictionary and passed to
:meth:`FileRunner.run` which will build a tree of step objects.

.. autoclass:: scriic.run.FileRunner
  :members:

.. module:: scriic.instruction

Outputting Steps
================

The generated tree of instructions contains the details to build a document in
whatever style you want. Whenever you display a step or insert it into a
document, you should set :attr:`Instruction.display_index` to a number or other
value which can be used to direct the user to look at this step.

.. autoclass:: scriic.instruction.Instruction
  :members: leaf_nodes, text

Exceptions
==========

.. automodule:: scriic.errors
  :members:
  :undoc-members:
