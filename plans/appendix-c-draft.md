## Appendix C: Bootstrap Schema Inventory

This appendix enumerates every construct the bootstrap schema-of-schemas (§12.3) defines. It serves as a checkable inventory: §11 remains the semantic authority for what each construct means; this appendix is the exhaustive authority for what constructs exist.

A discrepancy between §11 and this appendix is a defect to report (§1.3.1).

### C.1 ConceptDefinitions

The bootstrap schema defines the following 80 ConceptDefinitions.

Language-level traits (`id`, `key`, `reference`, `target`, `for`) are not listed in the Required Traits or Allowed Traits columns. Entity eligibility determines `id` availability; `key`, `reference`, `target`, and `for` must be explicitly authorized via TraitRules when used.

| Name | Kind | Entity | Required Traits | Allowed Traits | Required Children | Allowed Children | ExactlyOneChildOf | Spec Reference |
|------|------|--------|-----------------|----------------|-------------------|------------------|-------------------|----------------|
| AllOf | Structural | MustNotBeEntity | — | — | Rule (min=2) | — | — | §11.7.2 |
| AllowedValues | Structural | MustNotBeEntity | — | — | — | — | EnumeratedConstraint, ValueIsOneOf | §11.4.2 |
| AllowsChildConcept | Structural | MustNotBeEntity | conceptSelector | max, min | — | — | — | §11.3.4 |
| AllowsContent | Structural | MustNotBeEntity | whitespaceMode | — | — | — | — | §11.3.2 |
| AllowsTrait | Structural | MustNotBeEntity | name | — | — | AllowedValues (max=1) | — | §11.3.3 |
| AnyOf | Structural | MustNotBeEntity | — | — | Rule (min=2) | — | — | §11.7.3 |
| ChildConstraint | Structural | MustNotBeEntity | conceptSelector, type | — | — | — | — | §11.9.2 |
| ChildPath | Structural | MustNotBeEntity | conceptSelector | — | — | — | — | §11.8.1 |
| ChildRules | Structural | MustNotBeEntity | — | — | — | AllowsChildConcept, ExactlyOneChildOf, ForbidsChildConcept, RequiresChildConcept | — | §11.3.4 |
| ChildSatisfies | Structural | MustNotBeEntity | conceptSelector | — | Rule (min=1, max=1) | — | — | §11.9.2 |
| CollectionAllowsDuplicates | Structural | MustNotBeEntity | allowed | keyTrait | — | — | ChildPath, DescendantPath | §11.9.3 |
| CollectionAllowsEmpty | Structural | MustNotBeEntity | allowed | — | — | — | ChildPath, DescendantPath | §11.9.3 |
| CollectionOrdering | Structural | MustNotBeEntity | ordering | — | — | — | ChildPath, DescendantPath | §11.9.3 |
| CollectionRules | Structural | MustNotBeEntity | allowsDuplicates, ordering | — | — | — | — | §11.3.5 |
| ConceptDefinition | Structural | MustBeEntity | conceptKind, entityEligibility, name | description, role | — | ChildRules, CollectionRules, ContentRules, TraitRules | — | §11.3.1 |
| ConceptDefinitions | Structural | MustNotBeEntity | — | — | ConceptDefinition (min=1) | — | — | §11.3 |
| ConceptOption | Structural | MustNotBeEntity | conceptSelector | — | — | — | — | §11.3.4 |
| ConditionalConstraint | Structural | MustNotBeEntity | — | — | Then (min=1, max=1), When (min=1, max=1) | — | — | §11.7.5 |
| ConstraintDefinition | Structural | MustBeEntity | — | description, title | Rule (min=1, max=1), Targets (min=1, max=1) | — | — | §11.6.2 |
| ConstraintDefinitions | Structural | MustNotBeEntity | — | — | ConstraintDefinition (min=1) | — | — | §11.6.1 |
| ContentConstraint | Structural | MustNotBeEntity | type | flags, pattern | — | — | — | §11.9.10 |
| ContentPath | Structural | MustNotBeEntity | — | — | — | — | — | §11.8.1 |
| ContentRules | Structural | MustNotBeEntity | — | — | — | — | AllowsContent, ForbidsContent | §11.3.2 |
| ContextConstraint | Structural | MustNotBeEntity | type | contextSelector | — | — | — | §11.9.8 |
| Count | Structural | MustNotBeEntity | — | maxCount, minCount | — | — | — | §11.8.2 |
| DescendantPath | Structural | MustNotBeEntity | conceptSelector | — | — | — | — | §11.8.1 |
| EachMemberSatisfies | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | ChildPath, DescendantPath | §11.9.3 |
| EnumeratedConstraint | Structural | MustNotBeEntity | set | — | — | — | — | §11.4.2 |
| EnumeratedValueSet | Structural | MustBeEntity | name | description | Member (min=1) | — | — | §11.5.3 |
| EnumeratedValueSets | Structural | MustNotBeEntity | — | — | EnumeratedValueSet (min=1) | — | — | §11.5.3 |
| ExactlyOneChildOf | Structural | MustNotBeEntity | — | — | ConceptOption (min=2) | — | — | §11.3.4 |
| Exists | Structural | MustNotBeEntity | — | — | — | — | — | §11.8.2 |
| ForAll | Structural | MustNotBeEntity | — | — | — | — | — | §11.8.2 |
| ForbidsChildConcept | Structural | MustNotBeEntity | conceptSelector | — | — | — | — | §11.3.4 |
| ForbidsContent | Structural | MustNotBeEntity | — | — | — | — | — | §11.3.2 |
| ForbidsTrait | Structural | MustNotBeEntity | name | — | — | — | — | §11.3.3 |
| IdentityConstraint | Structural | MustNotBeEntity | type | flags, pattern, scope | — | — | — | §11.9.7 |
| Member | ValueLike | MustNotBeEntity | value | description, label | — | — | — | §11.5.3 |
| MemberCount | Structural | MustNotBeEntity | — | max, min | — | — | ChildPath, DescendantPath | §11.9.3 |
| Not | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | — | §11.7.4 |
| OnPathCount | Structural | MustNotBeEntity | — | maxCount, minCount | Rule (min=1, max=1) | — | ChildPath, ContentPath, DescendantPath, TraitPath | §9.5.3 |
| OnPathExists | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | ChildPath, ContentPath, DescendantPath, TraitPath | §9.5.3 |
| OnPathForAll | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | ChildPath, ContentPath, DescendantPath, TraitPath | §9.5.3 |
| OrderConstraint | Structural | MustNotBeEntity | byTrait, type | — | — | — | ChildPath, DescendantPath | §11.9.5 |
| PatternConstraint | Structural | MustNotBeEntity | pattern, trait | flags | — | — | — | §11.9.1 |
| RdfGraph | Structural | MustNotBeEntity | — | — | RdfTriple (min=1) | — | — | §9.6.1 |
| RdfTriple | Structural | MustNotBeEntity | predicate, subject | datatype, language, lexical, object | — | — | — | §9.6.1 |
| ReferenceConstraint | Structural | MustNotBeEntity | type | conceptSelector, traitName | — | — | — | §11.9.6 |
| RequiresChildConcept | Structural | MustNotBeEntity | conceptSelector | max, min | — | — | — | §11.3.4 |
| RequiresTrait | Structural | MustNotBeEntity | name | — | — | AllowedValues (max=1) | — | §11.3.3 |
| Rule | Structural | MustNotBeEntity | — | — | — | — | AllOf, AnyOf, ChildConstraint, ChildSatisfies, CollectionAllowsDuplicates, CollectionAllowsEmpty, CollectionOrdering, ConditionalConstraint, ContentConstraint, ContextConstraint, EachMemberSatisfies, IdentityConstraint, MemberCount, Not, OnPathCount, OnPathExists, OnPathForAll, OrderConstraint, PatternConstraint, ReferenceConstraint, TraitCardinality, TraitEquals, TraitExists, TraitLessOrEqual, TraitMissing, TraitValueType, UniqueConstraint, ValueInNumericRange, ValueIsNonEmpty, ValueIsOneOf, ValueIsValid, ValueLength, ValueMatchesPattern | §11.6.4 |
| Schema | Structural | MustBeEntity | authoringMode, compatibilityClass, namespace, version, versionScheme | description, title | — | ConceptDefinitions (max=1), ConstraintDefinitions (max=1), EnumeratedValueSets (max=1), RdfGraph (max=1), SchemaImports (max=1), TraitDefinitions (max=1), ValidatorDefinitions (max=1), ValueTypeDefinitions (max=1) | — | §11.2 |
| SchemaImport | Structural | MustNotBeEntity | namespace, reference | — | — | — | — | §11.2.1 |
| SchemaImports | Structural | MustNotBeEntity | — | — | SchemaImport (min=1) | — | — | §11.2.1 |
| TargetConcept | Structural | MustNotBeEntity | conceptSelector | — | — | — | — | §11.6.3.1 |
| TargetContext | Structural | MustNotBeEntity | contextSelector | — | — | — | — | §11.6.3.2 |
| Targets | Structural | MustNotBeEntity | — | — | — | TargetConcept, TargetContext | — | §11.6.3 |
| Then | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | — | §11.7.5 |
| TraitCardinality | Structural | MustNotBeEntity | trait | max, min | — | — | — | §11.9.1 |
| TraitDefinition | Structural | MustBeEntity | name | defaultValueType, defaultValueTypes, description, isReferenceTrait, priority | — | AllowedValues (max=1) | — | §11.4.1 |
| TraitDefinitions | Structural | MustNotBeEntity | — | — | TraitDefinition (min=1) | — | — | §11.4 |
| TraitEquals | Structural | MustNotBeEntity | trait, value | — | — | — | — | §11.9.1 |
| TraitExists | Structural | MustNotBeEntity | trait | — | — | — | — | §11.9.1 |
| TraitLessOrEqual | Structural | MustNotBeEntity | leftTrait, rightTrait | — | — | — | — | §11.9.1 |
| TraitMissing | Structural | MustNotBeEntity | trait | — | — | — | — | §11.9.1 |
| TraitPath | Structural | MustNotBeEntity | traitName | — | — | — | — | §11.8.1 |
| TraitRules | Structural | MustNotBeEntity | — | — | — | AllowsTrait, ForbidsTrait, RequiresTrait | — | §11.3.3 |
| TraitValueType | Structural | MustNotBeEntity | trait, valueType | — | — | — | — | §11.9.1 |
| UniqueConstraint | Structural | MustNotBeEntity | scope, trait | — | — | — | — | §11.9.4 |
| ValidatorDefinition | Structural | MustBeEntity | message, name | — | Content (RequiresContent) | — | — | §9.5.2 |
| ValidatorDefinitions | Structural | MustNotBeEntity | — | — | ValidatorDefinition (min=1) | — | — | §9.5.2 |
| ValueInNumericRange | Structural | MustNotBeEntity | — | max, min | — | — | — | §11.9.1 |
| ValueIsNonEmpty | Structural | MustNotBeEntity | — | — | — | — | — | §11.9.1 |
| ValueIsOneOf | Structural | MustNotBeEntity | values | — | — | — | — | §11.4.2 |
| ValueIsValid | Structural | MustNotBeEntity | validatorName | — | — | — | — | §11.9.1 |
| ValueLength | Structural | MustNotBeEntity | — | max, min | — | — | — | §11.9.1 |
| ValueMatchesPattern | Structural | MustNotBeEntity | pattern | flags | — | — | — | §11.9.1 |
| ValueTypeDefinition | Structural | MustBeEntity | baseValueType, name | validatorName | — | — | — | §11.5.2 |
| ValueTypeDefinitions | Structural | MustNotBeEntity | — | — | ValueTypeDefinition (min=1) | — | — | §11.5.2 |
| When | Structural | MustNotBeEntity | — | — | Rule (min=1, max=1) | — | — | §11.7.5 |

### C.2 TraitDefinitions

The bootstrap schema defines the following 49 TraitDefinitions.

| Name | Default Value Type | Allowed Values | Is Reference Trait | Spec Reference |
|------|-------------------|----------------|-------------------|----------------|
| allowed | $Boolean | — | No | §11.9.3 |
| allowsDuplicates | $Boolean | — | No | §11.3.5 |
| authoringMode | $EnumeratedToken | AuthoringMode | No | §11.2 |
| baseValueType | $ValueTypeExpression | — | No | §11.5.2 |
| byTrait | $TraitName | — | No | §11.9.5 |
| compatibilityClass | $EnumeratedToken | CompatibilityClass | No | §13.5 |
| conceptKind | $EnumeratedToken | ConceptKind | No | §11.3.1 |
| conceptSelector | $ConceptName | — | No | §11.3.4 |
| contextSelector | $ConceptName | — | No | §11.6.3.2 |
| datatype | $IriReference | — | No | §9.6.1 |
| defaultValueType | $ValueTypeExpression | — | No | §11.4.1 |
| defaultValueTypes | $ValueTypeExpression | — | No | §11.4.1 |
| description | $Text | — | No | §11.2 |
| entityEligibility | $EnumeratedToken | EntityEligibility | No | §11.3.1 |
| flags | $Text | — | No | §11.9.1 |
| isReferenceTrait | $Boolean | — | No | §11.4.1 |
| keyTrait | $TraitName | — | No | §11.9.3 |
| label | $Text | — | No | §11.5.3 |
| language | $Text | — | No | §9.6.1 |
| leftTrait | $TraitName | — | No | §11.9.1 |
| lexical | $Text | — | No | §9.6.1 |
| max | $NonNegativeInteger | — | No | §11.3.4 |
| maxCount | $NonNegativeInteger | — | No | §11.8.2 |
| message | $Text | — | No | §9.5.2 |
| min | $NonNegativeInteger | — | No | §11.3.4 |
| minCount | $NonNegativeInteger | — | No | §11.8.2 |
| name | $Text | — | No | §11.3.1 |
| namespace | $Text | — | No | §11.2 |
| object | $IriReference | — | No | §9.6.1 |
| ordering | $EnumeratedToken | Ordering | No | §11.3.5 |
| pattern | $Text | — | No | §11.9.1 |
| predicate | $IriReference | — | No | §9.6.1 |
| priority | $EnumeratedToken | — | No | §11.4.1 |
| rightTrait | $TraitName | — | No | §11.9.1 |
| role | $Text | — | No | §11.3.1 |
| scope | $ConceptName | — | No | §11.9.4 |
| set | $ConceptName | — | No | §11.4.2 |
| subject | $IriReference | — | No | §9.6.1 |
| title | $Text | — | No | §11.2 |
| trait | $TraitName | — | No | §11.9.1 |
| traitName | $TraitName | — | No | §11.8.1 |
| type | $EnumeratedToken | — | No | §11.9 |
| validatorName | $EnumeratedToken | — | No | §11.5.2 |
| value | $ValueExpression | — | No | §11.5.3 |
| values | $ValueExpression | — | No | §11.4.2 |
| valueType | $ValueTypeExpression | — | No | §11.9.1 |
| version | $Text | — | No | §13.3 |
| versionScheme | $EnumeratedToken | VersionScheme | No | §13.4.1 |
| whitespaceMode | $EnumeratedToken | WhitespaceMode | No | §11.3.2 |

### C.3 EnumeratedValueSets

The bootstrap schema defines the following 14 EnumeratedValueSets. Sets marked with (*) are built-in and MUST NOT be redefined by schemas (§11.5.4).

| Name | Members | Spec Reference |
|------|---------|----------------|
| AuthoringMode | $CanonicalMode, $SimplifiedMode | §9.4 |
| Cardinality (*) | $List, $Single | §11.5.4 |
| ChildConstraintType | $AllowsChildConcept, $ForbidsChildConcept, $RequiresChildConcept | §11.9.2 |
| CompatibilityClass (*) | $BackwardCompatible, $Breaking, $ForwardCompatible, $Initial | §13.5 |
| ConceptKind (*) | $Semantic, $Structural, $ValueLike | §11.3.1 |
| ContentConstraintType | $ContentMatchesPattern, $ContentRequired, $ForbidsContent | §11.9.10 |
| ContextConstraintType | $OnlyValidUnderContext, $OnlyValidUnderParent | §11.9.8 |
| EntityEligibility (*) | $MustBeEntity, $MustNotBeEntity | §11.3.1 |
| IdentityConstraintType | $IdentifierForm, $IdentifierUniqueness, $MustBeEntity, $MustNotBeEntity | §11.9.7 |
| OrderConstraintType | $Ascending, $Descending | §11.9.5 |
| Ordering (*) | $Ordered, $Unordered | §11.3.5 |
| ReferenceConstraintType | $ReferenceMustResolve, $ReferenceSingleton, $ReferenceTargetsConcept, $ReferenceTargetsEntity, $ReferenceTraitAllowed | §11.9.6 |
| VersionScheme | $DateYYYYMM, $DateYYYYMMDD, $Lexical, $Semver | §13.4.1 |
| WhitespaceMode | $Flow, $Preformatted | §11.3.2 |

### C.4 ConstraintDefinitions

The bootstrap schema defines the following 25 ConstraintDefinitions. These enforce structural well-formedness rules on the schema-definition concepts themselves.

| Constraint ID | Targets | Rule Summary | Spec Reference |
|---------------|---------|--------------|----------------|
| AllowsChildConcept | AllowsChildConcept | min must be less than or equal to max | §11.3.4 |
| ChildRules | ChildRules | At least one child of AllowsChildConcept, ExactlyOneChildOf, ForbidsChildConcept, or RequiresChildConcept | §11.3.4 |
| CollectionAllowsDuplicates | CollectionAllowsDuplicates | When allowed=false, keyTrait must be present | §11.9.3 |
| ConceptDefinition | ConceptDefinition | name must be unique within Schema | §11.3.1 |
| ContentConstraint | ContentConstraint | When type=$ContentMatchesPattern, pattern required; when type=$ContentRequired or $ForbidsContent, pattern and flags must be absent | §11.9.10 |
| ContextConstraint | ContextConstraint | When type=$OnlyValidUnderContext, contextSelector required; when type=$OnlyValidUnderParent, contextSelector must be absent | §11.9.8 |
| Count | Count | At least one of minCount or maxCount; minCount must be less than or equal to maxCount | §11.8.2 |
| EnumeratedValueSet | EnumeratedValueSet | name must be unique within Schema | §11.5.3 |
| IdentityConstraint | IdentityConstraint | When type=$IdentifierForm, pattern required; when type=$IdentifierUniqueness, scope required and pattern and flags must be absent; when type=$MustBeEntity or $MustNotBeEntity, scope, pattern, and flags must be absent | §11.9.7 |
| Member | Member | value must be unique within EnumeratedValueSet | §11.5.3 |
| MemberCount | MemberCount | At least one of min or max; min must be less than or equal to max | §11.9.3 |
| OnPathCount | OnPathCount | At least one of minCount or maxCount | §9.5.3 |
| RdfTriple | RdfTriple | Exactly one of object or lexical; datatype and language must not both be present | §9.6.1 |
| ReferenceConstraint | ReferenceConstraint | When type=$ReferenceTargetsConcept, conceptSelector required and traitName must be absent; when type=$ReferenceTraitAllowed, traitName required and conceptSelector must be absent; when type=$ReferenceMustResolve, $ReferenceSingleton, or $ReferenceTargetsEntity, conceptSelector and traitName must be absent | §11.9.6 |
| RequiresChildConcept | RequiresChildConcept | min must be less than or equal to max | §11.3.4 |
| Schema | Schema | When authoringMode=$SimplifiedMode, ConceptDefinitions required and RdfGraph forbidden; when authoringMode=$CanonicalMode, simplified-mode containers forbidden and RdfGraph required | §11.2 |
| Targets | Targets | At least one TargetConcept or TargetContext child | §11.6.3 |
| TraitCardinality | TraitCardinality | At least one of min or max; min must be less than or equal to max | §11.9.1 |
| TraitDefinition/nameUniqueness | TraitDefinition | name must be unique within Schema | §11.4.1 |
| TraitDefinition/valueTypeExclusivity | TraitDefinition | Exactly one of defaultValueType or defaultValueTypes | §11.4.1 |
| TraitRules | TraitRules | At least one child of AllowsTrait, ForbidsTrait, or RequiresTrait | §11.3.3 |
| ValidatorDefinition | ValidatorDefinition | name must be unique within Schema | §9.5.2 |
| ValueInNumericRange | ValueInNumericRange | At least one of min or max; min must be less than or equal to max | §11.9.1 |
| ValueLength | ValueLength | At least one of min or max; min must be less than or equal to max | §11.9.1 |
| ValueTypeDefinition | ValueTypeDefinition | name must be unique within Schema | §11.5.2 |

### C.5 ValueTypeDefinitions

The bootstrap schema defines the following 4 ValueTypeDefinitions.

| Name | Base Value Type | Validator | Spec Reference |
|------|----------------|-----------|----------------|
| ConceptName | $Text | — | §11.5.2 |
| TraitName | $Text | — | §11.5.2 |
| ValueExpression | $Text | — | §11.5.2 |
| ValueTypeExpression | $Text | — | §11.5.2 |

### C.6 Summary Counts

| Category | Count |
|----------|-------|
| ConceptDefinitions | 80 |
| TraitDefinitions | 49 |
| EnumeratedValueSets | 14 |
| ConstraintDefinitions | 25 |
| ValueTypeDefinitions | 4 |
