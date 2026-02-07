# Example

```cdx
[
  MARKDOWN:
  This file is an **exhaustive Codex surface-form example**.

  It intentionally exercises:
  - all value literal families (§5)
  - annotations (§8.9)
  - content vs children mode
  - identity and references
]

[GROUP: Metadata]

<Schema
	id=urn:codex:example:1.0.0
	version="1.0.0"
	title="Codex Highlighting Example"
	published={2026-01-29}
	revision=1p0
	active=true
	theme=&rebeccapurple
	background=color(display-p3 0.2 0.4 0.6)
	uuid=123e4567-e89b-12d3-a456-426614174000
	rangeExample=1..10
	rangeWithStep=0..1s0.1
>
	[
	  FLOW:
	  This schema exists only to demonstrate syntax highlighting.
	  It has **content**, not children.
	]
</Schema>

[END: Metadata]


[ This is a general annotation, not attached to anything. ]


[GROUP: Concepts]

[ Attached annotation for Person ]
<Person
	id=person:alice
	key=~alice
	name="Alice"
	nickname=`  Alice   Liddell  `
	initial='A'
	age=30
	height=1.65
	score=9.81e0
	precisionScore=9.810p3
	infiniteValue=Infinity
	negativeInfinite=-Infinity
	birthDate={1995-05-01}
	favoriteColor=#ff8800
	accentColor=&cornflowerblue
	palette=color-mix(in srgb, red 50%, blue)
	status=$Active
	reference=person:bob
>
	Born in Oxford.

	Likes tea, logic, and well-formed grammars.
</Person>


<Person
	id=person:bob
	key=~bob
	name="Bob"
	initial='B'
	age=-0
	rangeOfLetters='a'..'z'
	rangeOfDates={2024-01-01}..{2024-12-31}s7
	tags=set[$Friend, $Colleague]
	scores=[1, 2, 3.5, 4p0]
	attributes=map[
		height: 1.82,
		verified: true,
		color: &black
	]
	location=(51.7520, -1.2577)
>
	Bob prefers children mode.
</Person>

[END: Concepts]


[GROUP: Policies]

<LabelPolicy
	id=policy:labels
	for=concept:Person
	enabled=true
	validFor={now}
>
	[
	  CODE:
	  sh:message "Every Person must have a label."
	]
</LabelPolicy>

[END: Policies]


[GROUP: References]

<Tag
	id=tag:example
	target=~alice
	name=$Example
	color=hsl(280 50% 50%)
/>

[END: References]
```
