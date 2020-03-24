# Scriic Reference

## HOWTO ...

All scriics must begin with the `HOWTO` keyword followed by a clear, concise,
but descriptive title for the task being described.

Parameters can be accepted by enclosing a variable name in angle brackets. Try
to take as many things as parameters as possible to avoid duplicating tasks,
but also do not take parameters which would make the task significantly
different (this should be created as a separate task).

```
HOWTO Make a <filling> sandwich on <surface>
```

Notice how we take care to be extra-specific with where the sandwich will be
made.

## DO ...

This is the fundamental building block of scriics. It represents a simple text
instruction to the user.

```
DO Raise your arm above head height.
```

Variables can be substituted in by surrounding them in square brackets:

```
DO Multiply the numbers [num_one] and [num_two].
```

## SET ... DOING ...

This is a more advanced instruction which allows you to ask the user to measure,
observe or calculate a value, and then store that value in a variable for later
use.

```
SET filling DOING Choose your favourite filling of sandwich.
```

## SUB ...

This instruction allows you to import and run steps from another scriic. It
should be used wherever you include a step that could be re-used elsewhere.

```
SUB ./switch_light_on.scriic
```

File paths are relative to the current script.

## WITH ... AS ...

This must appear after `SUB` to pass in parameters.

```
SUB ./switch_light_on.scriic
WITH the main light switch AS switch
```

The same variable substitution rules as `DO` apply to the text after `WITH`:

```
SUB ./add_filling_to_sandwich.scriic
WITH [filling] AS filling
WITH the slice of bread which was placed onto [surface] AS bread
GO
```

## GO

This commits the parameters you have specified using `WITH` and launches the
subscriic. If the subscriic takes no parameters, `GO` will be implicitly called
and you should not include it.
