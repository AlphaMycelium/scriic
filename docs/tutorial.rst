Getting Started
***************

This is a short introduction to Scriic. For more in-depth information and
additional commands not described here, see :ref:`scriic-syntax`.

Basics
======

A Scriic is a short set of instructions written using the Scriic language,
with a ``.scriic`` file extension. Here's an example::

    HOWTO Calculate 1 + 1
    DO Add 1 to 1

All Scriics begin with the :ref:`HOWTO` line. This gives the instructions a
title, and can also include editable parameters::

    HOWTO Calculate <num1> + <num2>
    DO Add [num1] to [num2]

Parameters are stored in a variable, which can then be substituted into
later instructions using square brackets.

You can add many :ref:`DO` lines to create a list of steps. Each step should
normally only be a single sentence, but as specific as possible. If you end
up with more than one sentence in a step, it is normally a good idea to split
it into multiple steps.

Measure, Observe, Calculate
===========================

If you need to use a value which could change, ask the user to observe it, and
store the result in a variable::

    filling = DO Choose your favourite filling of sandwich

You can substitute the variable in the same way as we did for the parameters
before::

    DO Get some [filling] and place it on top of the bread

Subscriics
==========

Often, an instruction can contain more detailed steps inside it. This is where
*subscriics* come into play. A subscriic is written in a separate file, and
then used with the :ref:`SUB` instruction. The subscriic is also a valid Scriic
in itself. You can think of it like creating a function in other programming
languages.

For example, if you are writing instructions for a cheese sandwich, "butter
the bread" would be a good subscriic. It is something which could be useful
on its own, or to re-use in other Scriics.

::

    SUB ./subscriic.scriic

If the subscriic takes parameters, you need to give them on the lines below
using :ref:`WITH_AS` instructions::

    SUB ./subscriic.scriic
    WITH Foo AS parameter1
    WITH [bar] AS parameter2
    GO

You can substitute variables into the parameter input, too!

:ref:`GO` is used to say that you've finished the parameters and are ready to
run the subscriic. If the subscriic doesn't take any parameters, it will run
immediately and you don't need to write :ref:`GO`.

.. note::
  You can do a lot more with the :ref:`SUB` command, such as returning values.
  See :ref:`RETURN`.
