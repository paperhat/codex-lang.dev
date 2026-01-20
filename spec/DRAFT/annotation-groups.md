Status: DRAFT
Editor: Charles F. Munat

# Annotation Groups Extension

This document proposes an extension to the annotation syntax defined in
Surface Form Specification § 8.

## Motivation

Annotations must annotate something. The current spec requires an annotation
to appear directly above the Concept it annotates with no intervening blank line.

However, there is a valid use case for annotating a **group of sibling Concepts**
rather than a single Concept. For example, categorizing operators in a vocabulary
definition:

```cdx
<VocabularyDefinition id=codex:domain:behavior:math>
	<OperatorDefinition name="Add" ... />

	<OperatorDefinition name="Subtract" ... />

	<OperatorDefinition name="Sine" ... />

	<OperatorDefinition name="Cosine" ... />
</VocabularyDefinition>
```

Authors may wish to group "Add" and "Subtract" under "Arithmetic" and "Sine"
and "Cosine" under "Trigonometry" without creating additional wrapper Concepts.

## Proposed Syntax

### Group Start

```
[ GROUP: GroupName ]
```

### Group End

```
[ END: GroupName ]
```

### Rules

1. `GROUP:` and `END:` are case-sensitive keywords
2. The GroupName MUST match between GROUP and END
3. GroupName follows the same rules as annotation content (arbitrary text)
4. Groups MUST NOT overlap (proper nesting only)
5. Groups MAY be nested
6. A GROUP annotation MUST be followed by a blank line before the first Concept
7. An END annotation MUST be preceded by a blank line after the last Concept
8. Groups are structural metadata; they do not create new Concepts or Entities

### Example

```cdx
<VocabularyDefinition id=codex:domain:behavior:math>
	[ GROUP: Arithmetic ]

	<OperatorDefinition name="Add" ... />

	<OperatorDefinition name="Subtract" ... />

	[ END: Arithmetic ]

	[ GROUP: Trigonometry ]

	<OperatorDefinition name="Sine" ... />

	<OperatorDefinition name="Cosine" ... />

	[ END: Trigonometry ]
</VocabularyDefinition>
```

### Nested Groups

```cdx
[ GROUP: Math ]

[ GROUP: Basic ]

<OperatorDefinition name="Add" ... />

[ END: Basic ]

[ GROUP: Advanced ]

<OperatorDefinition name="Sine" ... />

[ END: Advanced ]

[ END: Math ]
```

## Canonical Form

In canonical form:

* GROUP and END annotations are preserved
* Whitespace within the annotation is normalized per existing rules
* The blank line after GROUP and before END is mandatory

## Distinction from Regular Annotations

Regular annotations attach to a single Concept:

```cdx
[This annotates Recipe]
<Recipe id=~pasta />
```

Group annotations define a range of sibling Concepts:

```cdx
[ GROUP: Italian Dishes ]

<Recipe id=~pasta />

<Recipe id=~risotto />

[ END: Italian Dishes ]
```

The `GROUP:` and `END:` prefixes distinguish group annotations from regular
annotations syntactically.

## Error Conditions

* `GROUP:` without matching `END:` → UnmatchedGroupAnnotation
* `END:` without matching `GROUP:` → UnmatchedEndAnnotation  
* `END: X` when innermost group is `GROUP: Y` → MismatchedGroupName
* Overlapping groups → OverlappingGroups

## Implementation Notes

Parsers MUST track open groups as a stack. When encountering `END:`, the
GroupName MUST match the top of the stack.

Group annotations are preserved in the AST as structural metadata but do not
affect the Concept hierarchy.
