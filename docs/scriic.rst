Scriic Syntax
*************

``HOWTO``
=========

Each Scriic file must contain a ``HOWTO`` line which gives the task a title.
It should be clear and concise, but specific.

Parameters can be accepted by enclosing a variable name in angle brackets. Try
to take as many things as parameters as possible to avoid duplicating tasks.
However, do not take parameters which would make the task significantly
different depending on their value (this should be created as a separate task).
::

    HOWTO Make a <filling> sandwich on <surface>

Notice how we take care to be extra-specific with where the sandwich will be
made.

.. note::
  It is conventional (and makes a lot of sense) to place this title line at the
  top of the file.

  However, it is technically possible to include it anywhere, and having more
  than one will cause the last defined value to be used. Variable values cannot
  be substituted into the title under any circumstances.

Place a ``"`` after the name of a parameter to enclose it in quotation marks::

  HOWTO Read <book_title">

The quotation marks will be omitted under certain circumstances, such as if
the value of the parameter is unknown (e.g. "the result of step 1").

``DO``
======

This is the fundamental building block of Scriic scripts. It represents a
simple text instruction::

    DO Raise your arm above head height.

Take care to be as specific as possible, and create as many ``DO`` lines as you
need. Each instruction should normally only be a single sentence.

Variables can be substituted in by surrounding them in square brackets::

    DO Multiply the numbers [num_one] and [num_two].

.. note::
  Similarly to in ``HOWTO``, you may place a ``"`` after the name of a variable
  to enclose it in quotation marks.

``SET DOING``
=============

This is a more advanced instruction which allows you to ask the user to
measure, observe or calculate a value, and then store that value in a variable
for later use. ::

    SET filling DOING Choose your favourite filling of sandwich.

``SUB``
=======

This instruction allows you to import and run steps from another Scriic file.
It should be used whenever you write a step that could be re-used elsewhere. ::

    SUB switch_light_on.scriic

File paths are relative to the current script. You can also load a file from a
Python package (installed via ``pip``)::

    SUB some_package:switch_light_on.scriic

``SUB INTO``
------------

Adding ``INTO`` after ``SUB`` allows you to receive a returned value from the
subscriic::

    SUB ./toggle_light.scriic INTO is_light_on

``RETURN``
==========

This sets the value to return when this scriic is called using ``SUB INTO``.
It does not actually end the execution. ::

    RETURN Some [value]

.. note::
  A second ``RETURN`` statement will overwrite the previous value.

``WITH AS``
===========

This is used after ``SUB`` to pass in any required parameters::

    SUB ./switch_light_on.scriic
    WITH the main light switch AS switch
    GO

The same variable substitution rules as ``DO`` apply to the input::

    SUB ./add_filling_to_sandwich.scriic
    WITH [filling] AS filling
    WITH the slice of bread which was placed onto [surface] AS bread
    GO

.. note::
  If you call ``WITH`` twice for the same parameter, it will be overwritten
  with the most recent value.

``GO``
------

This very simple command commits the parameters you have specified using
``WITH`` and launches the subscriic.


.. note::
  If the subscriic takes no parameters, ``GO`` will be implicitly called and
  you should not include it.

``REPEAT``
==========

Repeat for a certain number of times::

    REPEAT 5
      DO Something
    END

You can also use an amount from a variable name::

    SET times DOING Get a number of times to repeat
    REPEAT times
      DO Something
    END

.. warning::
  A runtime exception will be raised if a **known** variable value cannot be
  parsed as an integer.

``LETTERS IN``
==============

Loop over each letter in some text, storing the current letter in a variable. ::

    LETTERS char IN Hello
      DO Say "[char]"
    END

.. warning::
  ``LETTERS IN`` does not currently work with unknown values (originating
  from ``SET DOING``).

``END``
=======

This is used to end a code block after a looping or switching statement.
