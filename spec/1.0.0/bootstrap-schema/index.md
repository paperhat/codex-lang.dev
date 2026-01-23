Status: NORMATIVE  
Lock State: LOCKED  
Version: 0.1  
Editor: Charles F. Munat

# Codex Bootstrap Schema-of-Schemas

This document defines the bootstrap schema-of-schemas for Codex 1.0.0.

This schema is used to validate schema documents authored in Codex.
Every conforming implementation MUST include this schema as built-in, immutable data.

---

```cdx
<Schema
	id=urn:codex:bootstrap:1.0.0
	version="1.0.0"
	compatibilityClass=$BackwardCompatible
	authoringProfile=$ProfileA
	title="Codex Bootstrap Schema-of-Schemas"
	description="The authoritative schema for validating Codex schema documents."
>
	<EnumeratedValueSets>
		<EnumeratedValueSet name="ConceptKind">
			<Member value="Semantic" label="Semantic" description="A concept with domain meaning." />
			<Member value="Structural" label="Structural" description="A concept that organizes structure." />
			<Member value="ValueLike" label="Value-like" description="A concept that behaves like a value." />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="EntityEligibility">
			<Member value="MustBeEntity" label="Must be Entity" description="Instances MUST declare an id." />
			<Member value="MayBeEntity" label="May be Entity" description="Instances MAY declare an id." />
			<Member value="MustNotBeEntity" label="Must not be Entity" description="Instances MUST NOT declare an id." />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="CompatibilityClass">
			<Member value="BackwardCompatible" label="Backward Compatible" />
			<Member value="ForwardCompatible" label="Forward Compatible" />
			<Member value="Breaking" label="Breaking" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="AuthoringProfile">
			<Member value="ProfileA" label="Profile A" description="Layer A schema authoring only." />
			<Member value="ProfileB" label="Profile B" description="Layer B schema authoring only." />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="Ordering">
			<Member value="Ordered" label="Ordered" />
			<Member value="Unordered" label="Unordered" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="Cardinality">
			<Member value="Single" label="Single" />
			<Member value="List" label="List" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="ValueType">
			<Member value="String" />
			<Member value="Char" />
			<Member value="Boolean" />
			<Member value="Number" />
			<Member value="Integer" />
			<Member value="EnumeratedToken" />
			<Member value="IriReference" />
			<Member value="LookupToken" />
			<Member value="Uuid" />
			<Member value="Color" />
			<Member value="Temporal" />
			<Member value="List" />
			<Member value="Set" />
			<Member value="Map" />
			<Member value="Tuple" />
			<Member value="Range" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="ChildConstraintType">
			<Member value="RequiresChildConcept" />
			<Member value="AllowsChildConcept" />
			<Member value="ForbidsChildConcept" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="ReferenceConstraintType">
			<Member value="ReferenceTargetsEntity" />
			<Member value="ReferenceMustResolve" />
			<Member value="ReferenceTargetsConcept" />
			<Member value="ReferenceSingleton" />
			<Member value="ReferenceTraitAllowed" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="IdentityConstraintType">
			<Member value="MustBeEntity" />
			<Member value="MustNotBeEntity" />
			<Member value="IdentifierUniqueness" />
			<Member value="IdentifierForm" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="ContextConstraintType">
			<Member value="OnlyValidUnderParent" />
			<Member value="OnlyValidUnderContext" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="ContentConstraintType">
			<Member value="ContentForbiddenUnlessAllowed" />
			<Member value="ContentRequired" />
			<Member value="ContentMatchesPattern" />
		</EnumeratedValueSet>

		<EnumeratedValueSet name="TraitPriority">
			<Member value="Primary" />
			<Member value="Secondary" />
		</EnumeratedValueSet>
	</EnumeratedValueSets>

	<ConceptDefinitions>
		[GROUP: Root Schema Concept]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Schema
			key=~schema
			name="Schema"
			conceptKind=$Semantic
			entityEligibility=$MustBeEntity
		>
			<TraitRules>
				<RequiresTrait name="id" />
				<RequiresTrait name="version" />
				<RequiresTrait name="compatibilityClass" />
				<RequiresTrait name="authoringProfile" />
				<AllowsTrait name="title" />
				<AllowsTrait name="description" />
				<AllowsTrait name="key" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ConceptDefinitions" max=1 />
				<AllowsChildConcept conceptSelector="TraitDefinitions" max=1 />
				<AllowsChildConcept conceptSelector="EnumeratedValueSets" max=1 />
				<AllowsChildConcept conceptSelector="ConstraintDefinitions" max=1 />
				<AllowsChildConcept conceptSelector="ValidatorDefinitions" max=1 />
				<AllowsChildConcept conceptSelector="ValueTypeDefinitions" max=1 />
				<AllowsChildConcept conceptSelector="RdfGraph" max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Root Schema Concept]

		[GROUP: Definition Containers]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ConceptDefinitions
			key=~conceptDefinitions
			name="ConceptDefinitions"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ConceptDefinition" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitDefinitions
			key=~traitDefinitions
			name="TraitDefinitions"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="TraitDefinition" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:EnumeratedValueSets
			key=~enumeratedValueSets
			name="EnumeratedValueSets"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="EnumeratedValueSet" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ConstraintDefinitions
			key=~constraintDefinitions
			name="ConstraintDefinitions"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ConstraintDefinition" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValidatorDefinitions
			key=~validatorDefinitions
			name="ValidatorDefinitions"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ValidatorDefinition" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueTypeDefinitions
			key=~valueTypeDefinitions
			name="ValueTypeDefinitions"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ValueTypeDefinition" min=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Definition Containers]

		[GROUP: Concept Definition]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ConceptDefinition
			key=~conceptDefinition
			name="ConceptDefinition"
			conceptKind=$Semantic
			entityEligibility=$MustBeEntity
		>
			<TraitRules>
				<RequiresTrait name="id" />
				<RequiresTrait name="name" />
				<RequiresTrait name="conceptKind" />
				<RequiresTrait name="entityEligibility" />
				<AllowsTrait name="key" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ContentRules" max=1 />
				<AllowsChildConcept conceptSelector="TraitRules" max=1 />
				<AllowsChildConcept conceptSelector="ChildRules" max=1 />
				<AllowsChildConcept conceptSelector="CollectionRules" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ContentRules
			key=~contentRules
			name="ContentRules"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="AllowsContent" max=1 />
				<AllowsChildConcept conceptSelector="ForbidsContent" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AllowsContent
			key=~allowsContent
			name="AllowsContent"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		/>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ForbidsContent
			key=~forbidsContent
			name="ForbidsContent"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		/>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitRules
			key=~traitRules
			name="TraitRules"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="RequiresTrait" />
				<AllowsChildConcept conceptSelector="AllowsTrait" />
				<AllowsChildConcept conceptSelector="ForbidsTrait" />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:RequiresTrait
			key=~requiresTrait
			name="RequiresTrait"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="name" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AllowsTrait
			key=~allowsTrait
			name="AllowsTrait"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="name" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ForbidsTrait
			key=~forbidsTrait
			name="ForbidsTrait"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="name" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ChildRules
			key=~childRules
			name="ChildRules"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="AllowsChildConcept" />
				<AllowsChildConcept conceptSelector="RequiresChildConcept" />
				<AllowsChildConcept conceptSelector="ForbidsChildConcept" />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AllowsChildConcept
			key=~allowsChildConcept
			name="AllowsChildConcept"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:RequiresChildConcept
			key=~requiresChildConcept
			name="RequiresChildConcept"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ForbidsChildConcept
			key=~forbidsChildConcept
			name="ForbidsChildConcept"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:CollectionRules
			key=~collectionRules
			name="CollectionRules"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="ordering" />
				<RequiresTrait name="allowsDuplicates" />
			</TraitRules>
		</ConceptDefinition>

		[END: Concept Definition]

		[GROUP: Trait Definition]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitDefinition
			key=~traitDefinition
			name="TraitDefinition"
			conceptKind=$Semantic
			entityEligibility=$MayBeEntity
		>
			<TraitRules>
				<AllowsTrait name="id" />
				<RequiresTrait name="name" />
				<AllowsTrait name="defaultValueType" />
				<AllowsTrait name="defaultValueTypes" />
				<RequiresTrait name="cardinality" />
				<AllowsTrait name="itemValueType" />
				<AllowsTrait name="isReferenceTrait" />
				<AllowsTrait name="priority" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="AllowedValues" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AllowedValues
			key=~allowedValues
			name="AllowedValues"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ValueIsOneOf" />
				<AllowsChildConcept conceptSelector="EnumeratedConstraint" />
			</ChildRules>
		</ConceptDefinition>

		[END: Trait Definition]

		[GROUP: Enumerated Value Sets]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:EnumeratedValueSet
			key=~enumeratedValueSet
			name="EnumeratedValueSet"
			conceptKind=$Semantic
			entityEligibility=$MayBeEntity
		>
			<TraitRules>
				<AllowsTrait name="id" />
				<RequiresTrait name="name" />
			</TraitRules>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Member" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Member
			key=~member
			name="Member"
			conceptKind=$ValueLike
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="value" />
				<AllowsTrait name="label" />
				<AllowsTrait name="description" />
			</TraitRules>
		</ConceptDefinition>

		[END: Enumerated Value Sets]

		[GROUP: Value Type Definition]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueTypeDefinition
			key=~valueTypeDefinition
			name="ValueTypeDefinition"
			conceptKind=$Semantic
			entityEligibility=$MayBeEntity
		>
			<TraitRules>
				<AllowsTrait name="id" />
				<RequiresTrait name="name" />
				<RequiresTrait name="baseValueType" />
				<AllowsTrait name="validatorName" />
			</TraitRules>
		</ConceptDefinition>

		[END: Value Type Definition]

		[GROUP: Validator Definitions]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValidatorDefinition
			key=~validatorDefinition
			name="ValidatorDefinition"
			conceptKind=$Semantic
			entityEligibility=$MayBeEntity
		>
			<TraitRules>
				<RequiresTrait name="name" />
				<AllowsTrait name="message" />
			</TraitRules>
			<ContentRules>
				<AllowsContent />
			</ContentRules>
		</ConceptDefinition>

		[END: Validator Definitions]

		[GROUP: Constraint Definitions]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ConstraintDefinition
			key=~constraintDefinition
			name="ConstraintDefinition"
			conceptKind=$Semantic
			entityEligibility=$MustBeEntity
		>
			<TraitRules>
				<RequiresTrait name="id" />
				<AllowsTrait name="title" />
				<AllowsTrait name="description" />
			</TraitRules>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Targets" min=1 max=1 />
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Targets
			key=~targets
			name="Targets"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="TargetConcept" min=1 />
				<AllowsChildConcept conceptSelector="TargetContext" />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TargetConcept
			key=~targetConcept
			name="TargetConcept"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TargetContext
			key=~targetContext
			name="TargetContext"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="contextSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Rule
			key=~rule
			name="Rule"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="AllOf" max=1 />
				<AllowsChildConcept conceptSelector="AnyOf" max=1 />
				<AllowsChildConcept conceptSelector="Not" max=1 />
				<AllowsChildConcept conceptSelector="ConditionalConstraint" max=1 />
				<AllowsChildConcept conceptSelector="OnPathExists" max=1 />
				<AllowsChildConcept conceptSelector="OnPathForAll" max=1 />
				<AllowsChildConcept conceptSelector="OnPathCount" max=1 />
				<AllowsChildConcept conceptSelector="TraitExists" max=1 />
				<AllowsChildConcept conceptSelector="TraitMissing" max=1 />
				<AllowsChildConcept conceptSelector="TraitEquals" max=1 />
				<AllowsChildConcept conceptSelector="TraitCardinality" max=1 />
				<AllowsChildConcept conceptSelector="TraitValueType" max=1 />
				<AllowsChildConcept conceptSelector="ValueIsOneOf" max=1 />
				<AllowsChildConcept conceptSelector="ValueMatchesPattern" max=1 />
				<AllowsChildConcept conceptSelector="PatternConstraint" max=1 />
				<AllowsChildConcept conceptSelector="ValueLength" max=1 />
				<AllowsChildConcept conceptSelector="ValueInNumericRange" max=1 />
				<AllowsChildConcept conceptSelector="ValueIsNonEmpty" max=1 />
				<AllowsChildConcept conceptSelector="ValueIsValid" max=1 />
				<AllowsChildConcept conceptSelector="ChildConstraint" max=1 />
				<AllowsChildConcept conceptSelector="ChildSatisfies" max=1 />
				<AllowsChildConcept conceptSelector="CollectionOrdering" max=1 />
				<AllowsChildConcept conceptSelector="CollectionAllowsEmpty" max=1 />
				<AllowsChildConcept conceptSelector="CollectionAllowsDuplicates" max=1 />
				<AllowsChildConcept conceptSelector="MemberCount" max=1 />
				<AllowsChildConcept conceptSelector="EachMemberSatisfies" max=1 />
				<AllowsChildConcept conceptSelector="CollectionConstraint" max=1 />
				<AllowsChildConcept conceptSelector="UniqueConstraint" max=1 />
				<AllowsChildConcept conceptSelector="OrderConstraint" max=1 />
				<AllowsChildConcept conceptSelector="ReferenceConstraint" max=1 />
				<AllowsChildConcept conceptSelector="IdentityConstraint" max=1 />
				<AllowsChildConcept conceptSelector="ContextConstraint" max=1 />
				<AllowsChildConcept conceptSelector="ContentConstraint" max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Constraint Definitions]

		[GROUP: Rule Algebra]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AllOf
			key=~allOf
			name="AllOf"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=2 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:AnyOf
			key=~anyOf
			name="AnyOf"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=2 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Not
			key=~not
			name="Not"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ConditionalConstraint
			key=~conditionalConstraint
			name="ConditionalConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="When" min=1 max=1 />
				<RequiresChildConcept conceptSelector="Then" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:When
			key=~when
			name="When"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:Then
			key=~then
			name="Then"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Rule Algebra]

		[GROUP: Paths]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitPath
			key=~traitPath
			name="TraitPath"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="traitName" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ChildPath
			key=~childPath
			name="ChildPath"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:DescendantPath
			key=~descendantPath
			name="DescendantPath"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ContentPath
			key=~contentPath
			name="ContentPath"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		/>

		[END: Paths]

		[GROUP: Path-Scoped Rules]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:OnPathExists
			key=~onPathExists
			name="OnPathExists"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="TraitPath" max=1 />
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
				<AllowsChildConcept conceptSelector="ContentPath" max=1 />
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:OnPathForAll
			key=~onPathForAll
			name="OnPathForAll"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="TraitPath" max=1 />
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
				<AllowsChildConcept conceptSelector="ContentPath" max=1 />
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:OnPathCount
			key=~onPathCount
			name="OnPathCount"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<AllowsTrait name="minCount" />
				<AllowsTrait name="maxCount" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="TraitPath" max=1 />
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
				<AllowsChildConcept conceptSelector="ContentPath" max=1 />
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Path-Scoped Rules]

		[GROUP: Atomic Constraints - Trait]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitExists
			key=~traitExists
			name="TraitExists"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitMissing
			key=~traitMissing
			name="TraitMissing"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitEquals
			key=~traitEquals
			name="TraitEquals"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
				<RequiresTrait name="value" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitCardinality
			key=~traitCardinality
			name="TraitCardinality"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:TraitValueType
			key=~traitValueType
			name="TraitValueType"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
				<RequiresTrait name="valueType" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Trait]

		[GROUP: Atomic Constraints - Value]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueIsOneOf
			key=~valueIsOneOf
			name="ValueIsOneOf"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="values" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:EnumeratedConstraint
			key=~enumeratedConstraint
			name="EnumeratedConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="set" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueMatchesPattern
			key=~valueMatchesPattern
			name="ValueMatchesPattern"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="pattern" />
				<AllowsTrait name="flags" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:PatternConstraint
			key=~patternConstraint
			name="PatternConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
				<RequiresTrait name="pattern" />
				<AllowsTrait name="flags" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueLength
			key=~valueLength
			name="ValueLength"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueInNumericRange
			key=~valueInNumericRange
			name="ValueInNumericRange"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueIsNonEmpty
			key=~valueIsNonEmpty
			name="ValueIsNonEmpty"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		/>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ValueIsValid
			key=~valueIsValid
			name="ValueIsValid"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="validatorName" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Value]

		[GROUP: Atomic Constraints - Child]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ChildConstraint
			key=~childConstraint
			name="ChildConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ChildSatisfies
			key=~childSatisfies
			name="ChildSatisfies"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="conceptSelector" />
			</TraitRules>
			<ChildRules>
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Child]

		[GROUP: Atomic Constraints - Collection]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:CollectionOrdering
			key=~collectionOrdering
			name="CollectionOrdering"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="ordering" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:CollectionAllowsEmpty
			key=~collectionAllowsEmpty
			name="CollectionAllowsEmpty"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="allowed" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:CollectionAllowsDuplicates
			key=~collectionAllowsDuplicates
			name="CollectionAllowsDuplicates"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="allowed" />
				<AllowsTrait name="keyTrait" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:MemberCount
			key=~memberCount
			name="MemberCount"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<AllowsTrait name="min" />
				<AllowsTrait name="max" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:EachMemberSatisfies
			key=~eachMemberSatisfies
			name="EachMemberSatisfies"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
				<RequiresChildConcept conceptSelector="Rule" min=1 max=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:CollectionConstraint
			key=~collectionConstraint
			name="CollectionConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Collection]

		[GROUP: Atomic Constraints - Uniqueness and Order]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:UniqueConstraint
			key=~uniqueConstraint
			name="UniqueConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="trait" />
				<RequiresTrait name="scope" />
			</TraitRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:OrderConstraint
			key=~orderConstraint
			name="OrderConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
			</TraitRules>
			<ChildRules>
				<AllowsChildConcept conceptSelector="ChildPath" max=1 />
				<AllowsChildConcept conceptSelector="DescendantPath" max=1 />
			</ChildRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Uniqueness and Order]

		[GROUP: Atomic Constraints - Reference]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ReferenceConstraint
			key=~referenceConstraint
			name="ReferenceConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
				<AllowsTrait name="conceptSelector" />
				<AllowsTrait name="traitName" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Reference]

		[GROUP: Atomic Constraints - Identity]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:IdentityConstraint
			key=~identityConstraint
			name="IdentityConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Identity]

		[GROUP: Atomic Constraints - Context]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ContextConstraint
			key=~contextConstraint
			name="ContextConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
				<AllowsTrait name="contextSelector" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Context]

		[GROUP: Atomic Constraints - Content]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:ContentConstraint
			key=~contentConstraint
			name="ContentConstraint"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="type" />
				<AllowsTrait name="pattern" />
				<AllowsTrait name="flags" />
			</TraitRules>
		</ConceptDefinition>

		[END: Atomic Constraints - Content]

		[GROUP: Layer B - RDF Graph]

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:RdfGraph
			key=~rdfGraph
			name="RdfGraph"
			conceptKind=$Structural
			entityEligibility=$MustNotBeEntity
		>
			<ChildRules>
				<RequiresChildConcept conceptSelector="RdfTriple" min=1 />
			</ChildRules>
		</ConceptDefinition>

		<ConceptDefinition
			id=urn:codex:bootstrap:concept:RdfTriple
			key=~rdfTriple
			name="RdfTriple"
			conceptKind=$ValueLike
			entityEligibility=$MustNotBeEntity
		>
			<TraitRules>
				<RequiresTrait name="s" />
				<RequiresTrait name="p" />
				<AllowsTrait name="o" />
				<AllowsTrait name="lex" />
				<AllowsTrait name="datatype" />
				<AllowsTrait name="language" />
			</TraitRules>
		</ConceptDefinition>

		[END: Layer B - RDF Graph]
	</ConceptDefinitions>

	<TraitDefinitions>
		[GROUP: Common Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:id
			name="id"
			defaultValueType=$IriReference
			cardinality=$Single
			isReferenceTrait=false
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:key
			name="key"
			defaultValueType=$LookupToken
			cardinality=$Single
			isReferenceTrait=false
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:name
			name="name"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:title
			name="title"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:description
			name="description"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:version
			name="version"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:label
			name="label"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:value
			name="value"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:values
			name="values"
			defaultValueType=$List
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:message
			name="message"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		[END: Common Traits]

		[GROUP: Schema Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:compatibilityClass
			name="compatibilityClass"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="CompatibilityClass" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:authoringProfile
			name="authoringProfile"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="AuthoringProfile" />
			</AllowedValues>
		</TraitDefinition>

		[END: Schema Traits]

		[GROUP: Concept Definition Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:conceptKind
			name="conceptKind"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="ConceptKind" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:entityEligibility
			name="entityEligibility"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="EntityEligibility" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:conceptSelector
			name="conceptSelector"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:contextSelector
			name="contextSelector"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		[END: Concept Definition Traits]

		[GROUP: Trait Definition Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:defaultValueType
			name="defaultValueType"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="ValueType" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:defaultValueTypes
			name="defaultValueTypes"
			defaultValueType=$List
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:cardinality
			name="cardinality"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="Cardinality" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:itemValueType
			name="itemValueType"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Secondary
		>
			<AllowedValues>
				<EnumeratedConstraint set="ValueType" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:isReferenceTrait
			name="isReferenceTrait"
			defaultValueType=$Boolean
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:priority
			name="priority"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Secondary
		>
			<AllowedValues>
				<EnumeratedConstraint set="TraitPriority" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:baseValueType
			name="baseValueType"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="ValueType" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:validatorName
			name="validatorName"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		/>

		[END: Trait Definition Traits]

		[GROUP: Child Rule Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:min
			name="min"
			defaultValueType=$Integer
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:max
			name="max"
			defaultValueType=$Integer
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:minCount
			name="minCount"
			defaultValueType=$Integer
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:maxCount
			name="maxCount"
			defaultValueType=$Integer
			cardinality=$Single
			priority=$Secondary
		/>

		[END: Child Rule Traits]

		[GROUP: Collection Rule Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:ordering
			name="ordering"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="Ordering" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:allowsDuplicates
			name="allowsDuplicates"
			defaultValueType=$Boolean
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:allowed
			name="allowed"
			defaultValueType=$Boolean
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:keyTrait
			name="keyTrait"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		[END: Collection Rule Traits]

		[GROUP: Constraint Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:trait
			name="trait"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:traitName
			name="traitName"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:valueType
			name="valueType"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		>
			<AllowedValues>
				<EnumeratedConstraint set="ValueType" />
			</AllowedValues>
		</TraitDefinition>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:pattern
			name="pattern"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:flags
			name="flags"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:scope
			name="scope"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:set
			name="set"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:type
			name="type"
			defaultValueType=$EnumeratedToken
			cardinality=$Single
			priority=$Primary
		/>

		[END: Constraint Traits]

		[GROUP: RDF Triple Traits]

		<TraitDefinition
			id=urn:codex:bootstrap:trait:s
			name="s"
			defaultValueType=$IriReference
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:p
			name="p"
			defaultValueType=$IriReference
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:o
			name="o"
			defaultValueType=$IriReference
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:lex
			name="lex"
			defaultValueType=$String
			cardinality=$Single
			priority=$Primary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:datatype
			name="datatype"
			defaultValueType=$IriReference
			cardinality=$Single
			priority=$Secondary
		/>

		<TraitDefinition
			id=urn:codex:bootstrap:trait:language
			name="language"
			defaultValueType=$String
			cardinality=$Single
			priority=$Secondary
		/>

		[END: RDF Triple Traits]
	</TraitDefinitions>

	<ConstraintDefinitions>
		[GROUP: Schema Structural Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:schema-requires-concept-definitions
			title="Schema should have ConceptDefinitions"
			description="A meaningful schema should define at least one concept."
		>
			<Targets>
				<TargetConcept conceptSelector="Schema" />
			</Targets>
			<Rule>
				<ChildConstraint type=$RequiresChildConcept conceptSelector="ConceptDefinitions" />
			</Rule>
		</ConstraintDefinition>

		[END: Schema Structural Constraints]

		[GROUP: ContentRules Exclusivity]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:content-rules-exclusivity
			title="ContentRules must have exactly one child"
			description="ContentRules must contain either AllowsContent or ForbidsContent, not both."
		>
			<Targets>
				<TargetConcept conceptSelector="ContentRules" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<ChildConstraint type=$RequiresChildConcept conceptSelector="AllowsContent" />
							</Rule>
							<Rule>
								<ChildConstraint type=$ForbidsChildConcept conceptSelector="ForbidsContent" />
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<ChildConstraint type=$RequiresChildConcept conceptSelector="ForbidsContent" />
							</Rule>
							<Rule>
								<ChildConstraint type=$ForbidsChildConcept conceptSelector="AllowsContent" />
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		[END: ContentRules Exclusivity]

		[GROUP: Rule Exclusivity]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:rule-requires-operator
			title="Rule requires an operator child"
			description="Each Rule node must contain at least one rule operator child."
		>
			<Targets>
				<TargetConcept conceptSelector="Rule" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AnyOf" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="Not" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ConditionalConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathExists" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathForAll" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathCount" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitExists" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitMissing" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitEquals" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitCardinality" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitValueType" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsOneOf" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueMatchesPattern" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="PatternConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueLength" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueInNumericRange" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsNonEmpty" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsValid" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ChildConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ChildSatisfies" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionOrdering" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionAllowsEmpty" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionAllowsDuplicates" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="MemberCount" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="EachMemberSatisfies" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="UniqueConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OrderConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ReferenceConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="IdentityConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ContextConstraint" /></Rule>
					<Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ContentConstraint" /></Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:rule-forbids-multiple-operators
			title="Rule forbids multiple operator children"
			description="Each Rule node must not contain more than one rule operator child."
		>
			<Targets>
				<TargetConcept conceptSelector="Rule" />
			</Targets>
			<Rule>
				<AllOf>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AnyOf" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="Not" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ConditionalConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathExists" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathForAll" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OnPathCount" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitExists" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitMissing" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitEquals" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitCardinality" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="TraitValueType" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsOneOf" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueMatchesPattern" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="PatternConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueLength" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueInNumericRange" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsNonEmpty" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ValueIsValid" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ChildConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ChildSatisfies" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionOrdering" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionAllowsEmpty" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionAllowsDuplicates" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="MemberCount" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="EachMemberSatisfies" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="CollectionConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="UniqueConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="OrderConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ReferenceConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="IdentityConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ContextConstraint" /></Rule></AllOf></Rule></Not></Rule>
					<Rule><Not><Rule><AllOf><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="AllOf" /></Rule><Rule><ChildConstraint type=$RequiresChildConcept conceptSelector="ContentConstraint" /></Rule></AllOf></Rule></Not></Rule>
				</AllOf>
			</Rule>
		</ConstraintDefinition>

		[END: Rule Exclusivity]

		[GROUP: TraitDefinition Value Type Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:trait-definition-value-type
			title="TraitDefinition requires value type"
			description="A TraitDefinition must have either defaultValueType or defaultValueTypes, but not both."
		>
			<Targets>
				<TargetConcept conceptSelector="TraitDefinition" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<TraitExists trait="defaultValueType" />
							</Rule>
							<Rule>
								<TraitMissing trait="defaultValueTypes" />
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<TraitExists trait="defaultValueTypes" />
							</Rule>
							<Rule>
								<TraitMissing trait="defaultValueType" />
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:trait-definition-list-requires-item-type
			title="List cardinality requires itemValueType"
			description="When cardinality is List, itemValueType must be specified."
		>
			<Targets>
				<TargetConcept conceptSelector="TraitDefinition" />
			</Targets>
			<Rule>
				<ConditionalConstraint>
					<When>
						<TraitEquals trait="cardinality" value=$List />
					</When>
					<Then>
						<TraitExists trait="itemValueType" />
					</Then>
				</ConditionalConstraint>
			</Rule>
		</ConstraintDefinition>

		[END: TraitDefinition Value Type Constraints]

		[GROUP: RdfTriple Object Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:rdf-triple-object
			title="RdfTriple requires object"
			description="An RdfTriple must have either o (IRI object) or lex (literal lexical form), but not both."
		>
			<Targets>
				<TargetConcept conceptSelector="RdfTriple" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<TraitExists trait="o" />
							</Rule>
							<Rule>
								<TraitMissing trait="lex" />
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<TraitExists trait="lex" />
							</Rule>
							<Rule>
								<TraitMissing trait="o" />
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:rdf-triple-language-excludes-datatype
			title="RdfTriple language excludes datatype"
			description="If language is present, datatype must be absent."
		>
			<Targets>
				<TargetConcept conceptSelector="RdfTriple" />
			</Targets>
			<Rule>
				<ConditionalConstraint>
					<When>
						<TraitExists trait="language" />
					</When>
					<Then>
						<TraitMissing trait="datatype" />
					</Then>
				</ConditionalConstraint>
			</Rule>
		</ConstraintDefinition>

		[END: RdfTriple Object Constraints]

		[GROUP: Cardinality Constraint Bounds]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:value-length-requires-bound
			title="ValueLength requires at least one bound"
			description="ValueLength must have min or max (or both)."
		>
			<Targets>
				<TargetConcept conceptSelector="ValueLength" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<TraitExists trait="min" />
					</Rule>
					<Rule>
						<TraitExists trait="max" />
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:value-in-numeric-range-requires-bound
			title="ValueInNumericRange requires at least one bound"
			description="ValueInNumericRange must have min or max (or both)."
		>
			<Targets>
				<TargetConcept conceptSelector="ValueInNumericRange" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<TraitExists trait="min" />
					</Rule>
					<Rule>
						<TraitExists trait="max" />
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:trait-cardinality-requires-bound
			title="TraitCardinality requires at least one bound"
			description="TraitCardinality must have min or max (or both)."
		>
			<Targets>
				<TargetConcept conceptSelector="TraitCardinality" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<TraitExists trait="min" />
					</Rule>
					<Rule>
						<TraitExists trait="max" />
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:member-count-requires-bound
			title="MemberCount requires at least one bound"
			description="MemberCount must have min or max (or both)."
		>
			<Targets>
				<TargetConcept conceptSelector="MemberCount" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<TraitExists trait="min" />
					</Rule>
					<Rule>
						<TraitExists trait="max" />
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:on-path-count-requires-bound
			title="OnPathCount requires at least one bound"
			description="OnPathCount must have minCount or maxCount (or both)."
		>
			<Targets>
				<TargetConcept conceptSelector="OnPathCount" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<TraitExists trait="minCount" />
					</Rule>
					<Rule>
						<TraitExists trait="maxCount" />
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		[END: Cardinality Constraint Bounds]

		[GROUP: Path-Scoped Rule Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:on-path-exists-requires-path
			title="OnPathExists requires exactly one path"
			description="OnPathExists must contain exactly one path child (TraitPath, ChildPath, DescendantPath, or ContentPath)."
		>
			<Targets>
				<TargetConcept conceptSelector="OnPathExists" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="TraitPath" />
									<Rule>
										<TraitExists trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ChildPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="DescendantPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ContentPath" />
									<Rule>
										<TraitMissing trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:on-path-for-all-requires-path
			title="OnPathForAll requires exactly one path"
			description="OnPathForAll must contain exactly one path child (TraitPath, ChildPath, DescendantPath, or ContentPath)."
		>
			<Targets>
				<TargetConcept conceptSelector="OnPathForAll" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="TraitPath" />
									<Rule>
										<TraitExists trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ChildPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="DescendantPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ContentPath" />
									<Rule>
										<TraitMissing trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:on-path-count-requires-path
			title="OnPathCount requires exactly one path"
			description="OnPathCount must contain exactly one path child (TraitPath, ChildPath, DescendantPath, or ContentPath)."
		>
			<Targets>
				<TargetConcept conceptSelector="OnPathCount" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="TraitPath" />
									<Rule>
										<TraitExists trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ChildPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="DescendantPath" />
									<Rule>
										<TraitExists trait="conceptSelector" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ContentPath" />
											<Rule>
												<TraitMissing trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<OnPathExists>
									<ChildPath conceptSelector="ContentPath" />
									<Rule>
										<TraitMissing trait="traitName" />
									</Rule>
								</OnPathExists>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="TraitPath" />
											<Rule>
												<TraitExists trait="traitName" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="ChildPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
							<Rule>
								<Not>
									<Rule>
										<OnPathExists>
											<ChildPath conceptSelector="DescendantPath" />
											<Rule>
												<TraitExists trait="conceptSelector" />
											</Rule>
										</OnPathExists>
									</Rule>
								</Not>
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:collection-constraints-require-path
			title="Collection constraints require exactly one member path"
			description="CollectionOrdering, CollectionAllowsEmpty, CollectionAllowsDuplicates, MemberCount, EachMemberSatisfies, and OrderConstraint must contain exactly one member-selection path child (ChildPath or DescendantPath)."
		>
			<Targets>
				<TargetConcept conceptSelector="CollectionOrdering" />
				<TargetConcept conceptSelector="CollectionAllowsEmpty" />
				<TargetConcept conceptSelector="CollectionAllowsDuplicates" />
				<TargetConcept conceptSelector="MemberCount" />
				<TargetConcept conceptSelector="EachMemberSatisfies" />
				<TargetConcept conceptSelector="OrderConstraint" />
			</Targets>
			<Rule>
				<AnyOf>
					<Rule>
						<AllOf>
							<Rule>
								<ChildConstraint type=$RequiresChildConcept conceptSelector="ChildPath" />
							</Rule>
							<Rule>
								<ChildConstraint type=$ForbidsChildConcept conceptSelector="DescendantPath" />
							</Rule>
						</AllOf>
					</Rule>
					<Rule>
						<AllOf>
							<Rule>
								<ChildConstraint type=$RequiresChildConcept conceptSelector="DescendantPath" />
							</Rule>
							<Rule>
								<ChildConstraint type=$ForbidsChildConcept conceptSelector="ChildPath" />
							</Rule>
						</AllOf>
					</Rule>
				</AnyOf>
			</Rule>
		</ConstraintDefinition>

		[END: Path-Scoped Rule Constraints]

		[GROUP: Uniqueness Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:concept-definition-name-unique
			title="ConceptDefinition names must be unique"
			description="Within a schema, each ConceptDefinition must have a unique name."
		>
			<Targets>
				<TargetConcept conceptSelector="ConceptDefinition" />
			</Targets>
			<Rule>
				<UniqueConstraint trait="name" scope="Schema" />
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:trait-definition-name-unique
			title="TraitDefinition names must be unique"
			description="Within a schema, each TraitDefinition must have a unique name."
		>
			<Targets>
				<TargetConcept conceptSelector="TraitDefinition" />
			</Targets>
			<Rule>
				<UniqueConstraint trait="name" scope="Schema" />
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:enumerated-value-set-name-unique
			title="EnumeratedValueSet names must be unique"
			description="Within a schema, each EnumeratedValueSet must have a unique name."
		>
			<Targets>
				<TargetConcept conceptSelector="EnumeratedValueSet" />
			</Targets>
			<Rule>
				<UniqueConstraint trait="name" scope="Schema" />
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:member-value-unique
			title="Member values must be unique within set"
			description="Within an EnumeratedValueSet, each Member must have a unique value."
		>
			<Targets>
				<TargetConcept conceptSelector="Member" />
			</Targets>
			<Rule>
				<UniqueConstraint trait="value" scope="EnumeratedValueSet" />
			</Rule>
		</ConstraintDefinition>

		[END: Uniqueness Constraints]

		[GROUP: Profile Constraints]

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:profile-a-no-rdf-graph
			title="Profile A schemas must not contain RdfGraph"
			description="When authoringProfile is ProfileA, the schema must not contain an RdfGraph."
		>
			<Targets>
				<TargetConcept conceptSelector="Schema" />
			</Targets>
			<Rule>
				<ConditionalConstraint>
					<When>
						<TraitEquals trait="authoringProfile" value=$ProfileA />
					</When>
					<Then>
						<ChildConstraint type=$ForbidsChildConcept conceptSelector="RdfGraph" />
					</Then>
				</ConditionalConstraint>
			</Rule>
		</ConstraintDefinition>

		<ConstraintDefinition
			id=urn:codex:bootstrap:constraint:profile-b-requires-rdf-graph
			title="Profile B schemas must contain RdfGraph"
			description="When authoringProfile is ProfileB, the schema must contain exactly one RdfGraph."
		>
			<Targets>
				<TargetConcept conceptSelector="Schema" />
			</Targets>
			<Rule>
				<ConditionalConstraint>
					<When>
						<TraitEquals trait="authoringProfile" value=$ProfileB />
					</When>
					<Then>
						<ChildConstraint type=$RequiresChildConcept conceptSelector="RdfGraph" />
					</Then>
				</ConditionalConstraint>
			</Rule>
		</ConstraintDefinition>

		[END: Profile Constraints]
	</ConstraintDefinitions>
</Schema>
```

---

## Notes

1. This schema is self-describing: it defines all the constructs it uses.

2. The schema uses Profile A (`authoringProfile=$ProfileA`) as it is authored in Codex-native form.

3. All concept definitions include deterministic IRIs under the `urn:codex:bootstrap:` namespace.

4. Lookup tokens (`key` traits) are provided for all concepts to enable `~conceptName` references.

5. The constraint definitions enforce the invariants specified in §11 of the main specification, including:
   - ContentRules exclusivity (AllowsContent XOR ForbidsContent)
   - TraitDefinition value type requirements
   - RdfTriple object constraints
   - Cardinality bound requirements
   - Profile guardrails

6. Uniqueness constraints ensure concept, trait, and enumerated value set names are unique within their scopes.

7. This schema does NOT include runtime behavior, resolution, or execution semantics per the Codex non-goals.
