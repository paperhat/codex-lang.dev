## AllOf

### shape: urn:codex:bootstrap:1.0.0#AllOf#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AllOf
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#AllOf#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=2
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## AllowedValues

### shape: urn:codex:bootstrap:1.0.0#AllowedValues#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AllowedValues
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#AllowedValues#shape/xone/alt/7ce202e472a1935c760c7fe8ff8734a7e6e6340dd9bc5c13d74d500079448e78 | urn:codex:bootstrap:1.0.0#AllowedValues#shape/xone/alt/faa69cca183e34ba59b9f8e5764cc6992bf00f9619855a10ab03a6737430e7db
- child | urn:codex:bootstrap:1.0.0#AllowedValues#child/7ce202e472a1935c760c7fe8ff8734a7e6e6340dd9bc5c13d74d500079448e78 | class=urn:codex:bootstrap:1.0.0#EnumeratedConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#AllowedValues#child/faa69cca183e34ba59b9f8e5764cc6992bf00f9619855a10ab03a6737430e7db | class=urn:codex:bootstrap:1.0.0#ValueIsOneOf | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## AllowsChildConcept

### shape: urn:codex:bootstrap:1.0.0#AllowsChildConcept#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AllowsChildConcept
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1 | minInclusive=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1 | minInclusive=0

## AllowsContent

### shape: urn:codex:bootstrap:1.0.0#AllowsContent#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AllowsContent
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#whitespaceMode | min=1 | max=1 | in=[$Flow | $Preformatted]

## AllowsTrait

### shape: urn:codex:bootstrap:1.0.0#AllowsTrait#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AllowsTrait
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#AllowsTrait#child/0bd62a15e6910a4096a63e5b01ba0456f59ed50a4c727662f3ddb1e2117380a7 | class=urn:codex:bootstrap:1.0.0#AllowedValues
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## AnyOf

### shape: urn:codex:bootstrap:1.0.0#AnyOf#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#AnyOf
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#AnyOf#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=2
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ChildConstraint

### shape: urn:codex:bootstrap:1.0.0#ChildConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ChildConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$AllowsChildConcept | $ForbidsChildConcept | $RequiresChildConcept]

## ChildPath

### shape: urn:codex:bootstrap:1.0.0#ChildPath#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ChildPath
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## ChildRules

### shape: urn:codex:bootstrap:1.0.0#ChildRules#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ChildRules
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 | urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/2 | urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/3
- child | urn:codex:bootstrap:1.0.0#ChildRules#child/3e5d6a4f955e398de428d34bebbcfa21d76df97ac3743b2cdfe7aafbaff4ab4e | class=urn:codex:bootstrap:1.0.0#ForbidsChildConcept
- child | urn:codex:bootstrap:1.0.0#ChildRules#child/8ae62e6fbd1f1d1d86db9502c37dfc7911335bbc386137c3d8fe796aa5c7b36c | class=urn:codex:bootstrap:1.0.0#ExactlyOneChildOf
- child | urn:codex:bootstrap:1.0.0#ChildRules#child/9827b702a98ac1f4f96594e792e74ce92224989cd900e0b0ecf39f55e218dc7a | class=urn:codex:bootstrap:1.0.0#AllowsChildConcept
- child | urn:codex:bootstrap:1.0.0#ChildRules#child/f344fa80d57f2441b887f9c670bd50da15855ecaedbed45b3619e5d604d7d703 | class=urn:codex:bootstrap:1.0.0#RequiresChildConcept
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

### shape: urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#ChildRules#child/9827b702a98ac1f4f96594e792e74ce92224989cd900e0b0ecf39f55e218dc7a | min=1

### shape: urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#ChildRules#child/f344fa80d57f2441b887f9c670bd50da15855ecaedbed45b3619e5d604d7d703 | min=1

### shape: urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/2 (subshape)
- prop | urn:codex:bootstrap:1.0.0#ChildRules#child/3e5d6a4f955e398de428d34bebbcfa21d76df97ac3743b2cdfe7aafbaff4ab4e | min=1

### shape: urn:codex:bootstrap:1.0.0#ChildRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/3 (subshape)
- prop | urn:codex:bootstrap:1.0.0#ChildRules#child/8ae62e6fbd1f1d1d86db9502c37dfc7911335bbc386137c3d8fe796aa5c7b36c | min=1

## ChildSatisfies

### shape: urn:codex:bootstrap:1.0.0#ChildSatisfies#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ChildSatisfies
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ChildSatisfies#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## CollectionAllowsDuplicates

### shape: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- or: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- child | urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#allowed | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#keyTrait | datatype=urn:cdx:value-type:TraitName | max=1

### shape: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#allowed | hasValue=true

### shape: urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#keyTrait | min=1

## CollectionAllowsEmpty

### shape: urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- child | urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#allowed | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1

## CollectionOrdering

### shape: urn:codex:bootstrap:1.0.0#CollectionOrdering#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#CollectionOrdering
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#CollectionOrdering#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#CollectionOrdering#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- child | urn:codex:bootstrap:1.0.0#CollectionOrdering#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#CollectionOrdering#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#ordering | min=1 | max=1 | in=[$Ordered | $Unordered]

## CollectionRules

### shape: urn:codex:bootstrap:1.0.0#CollectionRules#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#CollectionRules
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#allowsDuplicates | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#ordering | min=1 | max=1 | in=[$Ordered | $Unordered]

## ConceptDefinition

### shape: urn:codex:bootstrap:1.0.0#ConceptDefinition#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConceptDefinition
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ConceptDefinition#child/295cc6d494ac0622f3c160d8ea5196e87ff95b81fdfcb049c91520eff0e1b8c6 | class=urn:codex:bootstrap:1.0.0#ChildRules
- child | urn:codex:bootstrap:1.0.0#ConceptDefinition#child/76c46cdf175fdefe2f32038b87834ee819b10087be2b16f32421ab871a77abcd | class=urn:codex:bootstrap:1.0.0#TraitRules
- child | urn:codex:bootstrap:1.0.0#ConceptDefinition#child/b747b15006f1056f768b42544164d9f2adbf80676fbb09af48d0d4f932b4bb42 | class=urn:codex:bootstrap:1.0.0#CollectionRules
- child | urn:codex:bootstrap:1.0.0#ConceptDefinition#child/c8e2941f9e04d816896a86c8f1a6b997031f5292e7a98123a19c9d52d145f4b0 | class=urn:codex:bootstrap:1.0.0#ContentRules
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptKind | min=1 | max=1 | in=[$Semantic | $Structural | $ValueLike]
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#entityEligibility | min=1 | max=1 | in=[$MustBeEntity | $MustNotBeEntity]
- trait | urn:codex:bootstrap:1.0.0#key | datatype=urn:cdx:value-type:LookupToken | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#role | datatype=http://www.w3.org/2001/XMLSchema#string | max=1

## ConceptDefinitions

### shape: urn:codex:bootstrap:1.0.0#ConceptDefinitions#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConceptDefinitions
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ConceptDefinitions#child/c223c1de24aacd3ce19f82703870880c5e886f098daa668d1723916f9856e7db | class=urn:codex:bootstrap:1.0.0#ConceptDefinition | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ConceptOption

### shape: urn:codex:bootstrap:1.0.0#ConceptOption#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConceptOption
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## ConditionalConstraint

### shape: urn:codex:bootstrap:1.0.0#ConditionalConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConditionalConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ConditionalConstraint#child/3d745e0fed6a77322d1cf1774c18705c73dd9512c8e633027c04213e97b1e288 | class=urn:codex:bootstrap:1.0.0#Then | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#ConditionalConstraint#child/cbf96509b0f6bad1035019f772279e8d24a809dad5e1c6144326f01fa235e9e1 | class=urn:codex:bootstrap:1.0.0#When | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ConstraintDefinition

### shape: urn:codex:bootstrap:1.0.0#ConstraintDefinition#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConstraintDefinition
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ConstraintDefinition#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#ConstraintDefinition#child/8a6a39c010373981170bdc5c74de7722d27b2b3eef7423688c007facaa9be0ae | class=urn:codex:bootstrap:1.0.0#Targets | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#title | datatype=http://www.w3.org/2001/XMLSchema#string | max=1

## ConstraintDefinitions

### shape: urn:codex:bootstrap:1.0.0#ConstraintDefinitions#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ConstraintDefinitions
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ConstraintDefinitions#child/07eaf5b19623e5d8f3ce333400b6e7b8846ab73d2a6e2d1f002df73a0f8c368d | class=urn:codex:bootstrap:1.0.0#ConstraintDefinition | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ContentConstraint

### shape: urn:codex:bootstrap:1.0.0#ContentConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ContentConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 | urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#flags | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#pattern | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$ContentMatchesPattern | $ContentRequired | $ForbidsContent]

### shape: urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#pattern | min=1
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ContentMatchesPattern

### shape: urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#flags | max=0
- prop | urn:codex:bootstrap:1.0.0#pattern | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ContentRequired

### shape: urn:codex:bootstrap:1.0.0#ContentConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2 (subshape)
- prop | urn:codex:bootstrap:1.0.0#flags | max=0
- prop | urn:codex:bootstrap:1.0.0#pattern | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ForbidsContent

## ContentPath

### shape: urn:codex:bootstrap:1.0.0#ContentPath#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ContentPath
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ContentRules

### shape: urn:codex:bootstrap:1.0.0#ContentRules#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ContentRules
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#ContentRules#shape/xone/alt/81635085895e4ed3f209da7519bba02de25595258eef03e30fb3058e7d75b2dd | urn:codex:bootstrap:1.0.0#ContentRules#shape/xone/alt/17d213f4cc54fe7519d8e8dc27b30c533e9a0c9a10785db206ebbd565e39f666
- child | urn:codex:bootstrap:1.0.0#ContentRules#child/17d213f4cc54fe7519d8e8dc27b30c533e9a0c9a10785db206ebbd565e39f666 | class=urn:codex:bootstrap:1.0.0#ForbidsContent | max=1
- child | urn:codex:bootstrap:1.0.0#ContentRules#child/81635085895e4ed3f209da7519bba02de25595258eef03e30fb3058e7d75b2dd | class=urn:codex:bootstrap:1.0.0#AllowsContent | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ContextConstraint

### shape: urn:codex:bootstrap:1.0.0#ContextConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ContextConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#ContextConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#ContextConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#contextSelector | datatype=urn:cdx:value-type:ConceptName | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$OnlyValidUnderContext | $OnlyValidUnderParent]

### shape: urn:codex:bootstrap:1.0.0#ContextConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#contextSelector | min=1
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$OnlyValidUnderContext

### shape: urn:codex:bootstrap:1.0.0#ContextConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#contextSelector | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$OnlyValidUnderParent

## Count

### shape: urn:codex:bootstrap:1.0.0#Count#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Count
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#Count#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#Count#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#maxCount | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#minCount | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1

### shape: urn:codex:bootstrap:1.0.0#Count#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#minCount | min=1

### shape: urn:codex:bootstrap:1.0.0#Count#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#maxCount | min=1

## DescendantPath

### shape: urn:codex:bootstrap:1.0.0#DescendantPath#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#DescendantPath
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## EachMemberSatisfies

### shape: urn:codex:bootstrap:1.0.0#EachMemberSatisfies#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#EachMemberSatisfies
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#EachMemberSatisfies#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#EachMemberSatisfies#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- child | urn:codex:bootstrap:1.0.0#EachMemberSatisfies#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#EachMemberSatisfies#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#EachMemberSatisfies#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## EnumeratedConstraint

### shape: urn:codex:bootstrap:1.0.0#EnumeratedConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#EnumeratedConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#set | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## EnumeratedValueSet

### shape: urn:codex:bootstrap:1.0.0#EnumeratedValueSet#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#EnumeratedValueSet
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#EnumeratedValueSet#child/af3c415500c865a5521972066e6314225442005155644d9b8e0a4485d73d5234 | class=urn:codex:bootstrap:1.0.0#Member | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#key | datatype=urn:cdx:value-type:LookupToken | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## EnumeratedValueSets

### shape: urn:codex:bootstrap:1.0.0#EnumeratedValueSets#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#EnumeratedValueSets
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#EnumeratedValueSets#child/0f73b140a484c03c5083fa09718eca3487c373fe551211a19d2abcc32b6fe652 | class=urn:codex:bootstrap:1.0.0#EnumeratedValueSet | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ExactlyOneChildOf

### shape: urn:codex:bootstrap:1.0.0#ExactlyOneChildOf#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ExactlyOneChildOf
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ExactlyOneChildOf#child/bd1dfd9c1c4404bb9d72a1dd9330f92f793a63b2faadd09e095b71b524cff542 | class=urn:codex:bootstrap:1.0.0#ConceptOption | min=2
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## Exists

### shape: urn:codex:bootstrap:1.0.0#Exists#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Exists
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ForAll

### shape: urn:codex:bootstrap:1.0.0#ForAll#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ForAll
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ForbidsChildConcept

### shape: urn:codex:bootstrap:1.0.0#ForbidsChildConcept#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ForbidsChildConcept
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## ForbidsContent

### shape: urn:codex:bootstrap:1.0.0#ForbidsContent#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ForbidsContent
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ForbidsTrait

### shape: urn:codex:bootstrap:1.0.0#ForbidsTrait#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ForbidsTrait
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## IdentityConstraint

### shape: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#IdentityConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 | urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2 | urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/3
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#flags | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#pattern | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#scope | datatype=urn:cdx:value-type:ConceptName | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$IdentifierForm | $IdentifierUniqueness | $MustBeEntity | $MustNotBeEntity]

### shape: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#pattern | min=1
- prop | urn:codex:bootstrap:1.0.0#scope | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$IdentifierForm

### shape: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#flags | max=0
- prop | urn:codex:bootstrap:1.0.0#pattern | max=0
- prop | urn:codex:bootstrap:1.0.0#scope | min=1
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$IdentifierUniqueness

### shape: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2 (subshape)
- prop | urn:codex:bootstrap:1.0.0#flags | max=0
- prop | urn:codex:bootstrap:1.0.0#pattern | max=0
- prop | urn:codex:bootstrap:1.0.0#scope | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$MustBeEntity

### shape: urn:codex:bootstrap:1.0.0#IdentityConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/3 (subshape)
- prop | urn:codex:bootstrap:1.0.0#flags | max=0
- prop | urn:codex:bootstrap:1.0.0#pattern | max=0
- prop | urn:codex:bootstrap:1.0.0#scope | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$MustNotBeEntity

## Member

### shape: urn:codex:bootstrap:1.0.0#Member#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Member
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#label | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#value | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## MemberCount

### shape: urn:codex:bootstrap:1.0.0#MemberCount#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#MemberCount
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#MemberCount#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#MemberCount#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- or: urn:codex:bootstrap:1.0.0#MemberCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#MemberCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- child | urn:codex:bootstrap:1.0.0#MemberCount#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#MemberCount#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1

### shape: urn:codex:bootstrap:1.0.0#MemberCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#min | min=1

### shape: urn:codex:bootstrap:1.0.0#MemberCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#max | min=1

## Not

### shape: urn:codex:bootstrap:1.0.0#Not#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Not
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#Not#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## OnPathCount

### shape: urn:codex:bootstrap:1.0.0#OnPathCount#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#OnPathCount
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#OnPathCount#shape/xone/alt/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | urn:codex:bootstrap:1.0.0#OnPathCount#shape/xone/alt/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | urn:codex:bootstrap:1.0.0#OnPathCount#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | urn:codex:bootstrap:1.0.0#OnPathCount#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca
- or: urn:codex:bootstrap:1.0.0#OnPathCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#OnPathCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- child | urn:codex:bootstrap:1.0.0#OnPathCount#child/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | class=urn:codex:bootstrap:1.0.0#ContentPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathCount#child/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | class=urn:codex:bootstrap:1.0.0#TraitPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathCount#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathCount#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathCount#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#maxCount | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#minCount | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1

### shape: urn:codex:bootstrap:1.0.0#OnPathCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#minCount | min=1

### shape: urn:codex:bootstrap:1.0.0#OnPathCount#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#maxCount | min=1

## OnPathExists

### shape: urn:codex:bootstrap:1.0.0#OnPathExists#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#OnPathExists
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#OnPathExists#shape/xone/alt/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | urn:codex:bootstrap:1.0.0#OnPathExists#shape/xone/alt/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | urn:codex:bootstrap:1.0.0#OnPathExists#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | urn:codex:bootstrap:1.0.0#OnPathExists#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca
- child | urn:codex:bootstrap:1.0.0#OnPathExists#child/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | class=urn:codex:bootstrap:1.0.0#ContentPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathExists#child/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | class=urn:codex:bootstrap:1.0.0#TraitPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathExists#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathExists#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathExists#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## OnPathForAll

### shape: urn:codex:bootstrap:1.0.0#OnPathForAll#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#OnPathForAll
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#OnPathForAll#shape/xone/alt/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | urn:codex:bootstrap:1.0.0#OnPathForAll#shape/xone/alt/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | urn:codex:bootstrap:1.0.0#OnPathForAll#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | urn:codex:bootstrap:1.0.0#OnPathForAll#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca
- child | urn:codex:bootstrap:1.0.0#OnPathForAll#child/01ed9f3ce9c123082de6760df71be57f9b207a0fbc812e30da7e3e1c88af08ec | class=urn:codex:bootstrap:1.0.0#ContentPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathForAll#child/19abd3ea6186f0def524810088b6eae5e8ad10f70e7955791c02e694bad422f3 | class=urn:codex:bootstrap:1.0.0#TraitPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathForAll#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathForAll#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#OnPathForAll#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## OrderConstraint

### shape: urn:codex:bootstrap:1.0.0#OrderConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#OrderConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#OrderConstraint#shape/xone/alt/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | urn:codex:bootstrap:1.0.0#OrderConstraint#shape/xone/alt/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f
- child | urn:codex:bootstrap:1.0.0#OrderConstraint#child/579a817d41e8bc8ecef7624b9a0cea22e02f449466b60618910d0820629c299f | class=urn:codex:bootstrap:1.0.0#DescendantPath | max=1
- child | urn:codex:bootstrap:1.0.0#OrderConstraint#child/7a4d2bec1c9fe9bcb05a954301827fc84f30a936e475197c4f94e74a809885ca | class=urn:codex:bootstrap:1.0.0#ChildPath | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#byTrait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$Ascending | $Descending]

## PatternConstraint

### shape: urn:codex:bootstrap:1.0.0#PatternConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#PatternConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#flags | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#pattern | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## RdfGraph

### shape: urn:codex:bootstrap:1.0.0#RdfGraph#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#RdfGraph
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#RdfGraph#child/7c0b35e593e04b2ed86e6a63336c104f439eab980fa3be0a096a68c7ba4c69b1 | class=urn:codex:bootstrap:1.0.0#RdfTriple | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## RdfTriple

### shape: urn:codex:bootstrap:1.0.0#RdfTriple#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#RdfTriple
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#RdfTriple#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#RdfTriple#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1
- not: urn:codex:bootstrap:1.0.0#RdfTriple#shape/not/6d9f0bc6a43fcf341c62365c2f21334ff4ce15d85c787f3776c0add8ea9d1e94
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#datatype | nodeKind=http://www.w3.org/ns/shacl#IRI | max=1
- trait | urn:codex:bootstrap:1.0.0#language | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#lexical | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#object | nodeKind=http://www.w3.org/ns/shacl#IRI | max=1
- trait | urn:codex:bootstrap:1.0.0#predicate | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#subject | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

### shape: urn:codex:bootstrap:1.0.0#RdfTriple#shape/not/6d9f0bc6a43fcf341c62365c2f21334ff4ce15d85c787f3776c0add8ea9d1e94 (subshape)
- prop | urn:codex:bootstrap:1.0.0#datatype | min=1
- prop | urn:codex:bootstrap:1.0.0#language | min=1

### shape: urn:codex:bootstrap:1.0.0#RdfTriple#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#datatype | max=0
- prop | urn:codex:bootstrap:1.0.0#language | max=0
- prop | urn:codex:bootstrap:1.0.0#lexical | max=0
- prop | urn:codex:bootstrap:1.0.0#object | min=1

### shape: urn:codex:bootstrap:1.0.0#RdfTriple#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#lexical | min=1
- prop | urn:codex:bootstrap:1.0.0#object | max=0

## ReferenceConstraint

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ReferenceConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 | urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2 | urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/3 | urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/4
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | max=1
- trait | urn:codex:bootstrap:1.0.0#traitName | datatype=urn:cdx:value-type:TraitName | max=1
- trait | urn:codex:bootstrap:1.0.0#type | min=1 | max=1 | in=[$ReferenceMustResolve | $ReferenceSingleton | $ReferenceTargetsConcept | $ReferenceTargetsEntity | $ReferenceTraitAllowed]

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#conceptSelector | min=1
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ReferenceTargetsConcept

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#traitName | min=1
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ReferenceTraitAllowed

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/2 (subshape)
- prop | urn:codex:bootstrap:1.0.0#conceptSelector | max=0
- prop | urn:codex:bootstrap:1.0.0#traitName | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ReferenceTargetsEntity

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/3 (subshape)
- prop | urn:codex:bootstrap:1.0.0#conceptSelector | max=0
- prop | urn:codex:bootstrap:1.0.0#traitName | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ReferenceMustResolve

### shape: urn:codex:bootstrap:1.0.0#ReferenceConstraint#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/4 (subshape)
- prop | urn:codex:bootstrap:1.0.0#conceptSelector | max=0
- prop | urn:codex:bootstrap:1.0.0#traitName | max=0
- prop | urn:codex:bootstrap:1.0.0#type | hasValue=$ReferenceSingleton

## RequiresChildConcept

### shape: urn:codex:bootstrap:1.0.0#RequiresChildConcept#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#RequiresChildConcept
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1 | minInclusive=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1 | minInclusive=1

## RequiresTrait

### shape: urn:codex:bootstrap:1.0.0#RequiresTrait#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#RequiresTrait
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#RequiresTrait#child/0bd62a15e6910a4096a63e5b01ba0456f59ed50a4c727662f3ddb1e2117380a7 | class=urn:codex:bootstrap:1.0.0#AllowedValues
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## Rule

### shape: urn:codex:bootstrap:1.0.0#Rule#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Rule
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/2d181a7256c178caff8cc4a08a203bbbc4879b0bac5e708aab18989972e3295f | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/0d7de4a830ecc1d318065b4c04610348c086b5d3db6a44802e3cc47372babea2 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/ecd7960f09fb061cda24e8997f49919e14545be8074977659b4e2926c4d3a226 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/ed10ad9d560720be8722ea1ca1d0bc45d26592dd81883e5665b1098adc39d4e9 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/e45f071809685f79d4f6f9bbe9809e0a45fa10477905769d7a13fff7dfc7ad10 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/aa02d116c68e797403dc18632c5d45ddd6c86050b22321a48bf7e4e8987c04df | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/0c4eaebc7894c1058d4c14b15a42669ad34011a0f285df51f4eb15eb571d1394 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/41a42d6304aee6d5ac4967c44705d19f7b89284b610b6d2721c011b340416496 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/d96b5be3c3b1950d911dfe98d7a41926b8646ff0594a4e48ed175ef7d3b808a6 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/4a61789f2da50a3f9ba754b14bc2ea51488d916f56bcdbd28137f4d1a2ce07a1 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/d168c84ff7f062f4d583177e96fc1689a04be4d67201e10ff3824aaacbc9caa9 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/887c2a73b3743cb3f78f98e9453ac0cd4bf7c254176d0e3a9e447372142bb559 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/af518f54351016b22fd23559a085960703e5517919b373374974e3fffab0dae2 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/7fe684e49a0557ee268441a53c8931f227e299afcaa05905e4e872f7b1a9f57b | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/48e27acd47b60a1083b0051c4b080dc44b137a1ee4d6485a90585fce8d34ff01 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/7e739ba81d88067608ae256ee71e888a5a2685c11337b17cc258379cefa7d79f | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/f852682a462b515853bc77cf48975160401ee999bd940eecbe64905548618feb | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/497bff9b8dbc7df438deb0cadb96535dc86d73cd62c4a8642ced11c7a925f431 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/110197796385eeb5d82820e31ec8ef36df98156a3abd97c7c476b95df082f7b0 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/56c97fb0172e185e262500f609949340da78071edb2ec8302ca2609da36ff7f5 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/25d7bb2e4e84a4f08d9a926fb861689cdbcc1b6c68ad1c72d818680d6bc4fc10 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/f1698a235d5d97b80ffd43e81afad4b15767feacb8916442622322da1459da8a | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/d513fa8d76d13418049d8c27df6c2440332084b88c2561f90bee2cfce15dc169 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/130aa5f535d046fe7fc9fedc4a1ad59a4408a396c751619010bf509968ee5979 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/c7323f032078cf8743aa2af5788c8cd70dfe416713bca727fd11a347a14afc40 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/a20c6c787c8f4ac10c8d88593fe90cd3d8a0e59369b63c78af239a1df70594ec | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/6b8aee57e1bc68584d8746ce56e726d3dd2d5bcef5f9c1a5e8bdf4afd2dd3634 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/dc637fc98d05b079818898ce0b868c47ba8a7c946851d4fe492320772468ddd3 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/980295c4a688db175d7781f501ae05f5556d842895e7cad24d27824b84a5ce28 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/faa69cca183e34ba59b9f8e5764cc6992bf00f9619855a10ab03a6737430e7db | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/8212dfb038e0b2c5e48d14a56d588af3e0fdcc3d2616e56fe0fe727ebd3b4e92 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/e6f3a77e00b7e43cc3fd086d672062ed416fb016b19e5854d9197f8d5ce4f1d8 | urn:codex:bootstrap:1.0.0#Rule#shape/xone/alt/5e83c2c7c08eda22c90678aa74cdf31aeefa3838af6a46f146bfc6f7ccff5094
- child | urn:codex:bootstrap:1.0.0#Rule#child/0c4eaebc7894c1058d4c14b15a42669ad34011a0f285df51f4eb15eb571d1394 | class=urn:codex:bootstrap:1.0.0#CollectionOrdering | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/0d7de4a830ecc1d318065b4c04610348c086b5d3db6a44802e3cc47372babea2 | class=urn:codex:bootstrap:1.0.0#AnyOf | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/110197796385eeb5d82820e31ec8ef36df98156a3abd97c7c476b95df082f7b0 | class=urn:codex:bootstrap:1.0.0#PatternConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/130aa5f535d046fe7fc9fedc4a1ad59a4408a396c751619010bf509968ee5979 | class=urn:codex:bootstrap:1.0.0#TraitLessOrEqual | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/25d7bb2e4e84a4f08d9a926fb861689cdbcc1b6c68ad1c72d818680d6bc4fc10 | class=urn:codex:bootstrap:1.0.0#TraitCardinality | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/2d181a7256c178caff8cc4a08a203bbbc4879b0bac5e708aab18989972e3295f | class=urn:codex:bootstrap:1.0.0#AllOf | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/41a42d6304aee6d5ac4967c44705d19f7b89284b610b6d2721c011b340416496 | class=urn:codex:bootstrap:1.0.0#ConditionalConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/48e27acd47b60a1083b0051c4b080dc44b137a1ee4d6485a90585fce8d34ff01 | class=urn:codex:bootstrap:1.0.0#OnPathCount | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/497bff9b8dbc7df438deb0cadb96535dc86d73cd62c4a8642ced11c7a925f431 | class=urn:codex:bootstrap:1.0.0#OrderConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/4a61789f2da50a3f9ba754b14bc2ea51488d916f56bcdbd28137f4d1a2ce07a1 | class=urn:codex:bootstrap:1.0.0#ContextConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/56c97fb0172e185e262500f609949340da78071edb2ec8302ca2609da36ff7f5 | class=urn:codex:bootstrap:1.0.0#ReferenceConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/5e83c2c7c08eda22c90678aa74cdf31aeefa3838af6a46f146bfc6f7ccff5094 | class=urn:codex:bootstrap:1.0.0#ValueMatchesPattern | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/6b8aee57e1bc68584d8746ce56e726d3dd2d5bcef5f9c1a5e8bdf4afd2dd3634 | class=urn:codex:bootstrap:1.0.0#UniqueConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/7e739ba81d88067608ae256ee71e888a5a2685c11337b17cc258379cefa7d79f | class=urn:codex:bootstrap:1.0.0#OnPathExists | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/7fe684e49a0557ee268441a53c8931f227e299afcaa05905e4e872f7b1a9f57b | class=urn:codex:bootstrap:1.0.0#Not | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/8212dfb038e0b2c5e48d14a56d588af3e0fdcc3d2616e56fe0fe727ebd3b4e92 | class=urn:codex:bootstrap:1.0.0#ValueIsValid | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/887c2a73b3743cb3f78f98e9453ac0cd4bf7c254176d0e3a9e447372142bb559 | class=urn:codex:bootstrap:1.0.0#IdentityConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/980295c4a688db175d7781f501ae05f5556d842895e7cad24d27824b84a5ce28 | class=urn:codex:bootstrap:1.0.0#ValueIsNonEmpty | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/a20c6c787c8f4ac10c8d88593fe90cd3d8a0e59369b63c78af239a1df70594ec | class=urn:codex:bootstrap:1.0.0#TraitValueType | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/aa02d116c68e797403dc18632c5d45ddd6c86050b22321a48bf7e4e8987c04df | class=urn:codex:bootstrap:1.0.0#CollectionAllowsEmpty | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/af518f54351016b22fd23559a085960703e5517919b373374974e3fffab0dae2 | class=urn:codex:bootstrap:1.0.0#MemberCount | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/c7323f032078cf8743aa2af5788c8cd70dfe416713bca727fd11a347a14afc40 | class=urn:codex:bootstrap:1.0.0#TraitMissing | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/d168c84ff7f062f4d583177e96fc1689a04be4d67201e10ff3824aaacbc9caa9 | class=urn:codex:bootstrap:1.0.0#EachMemberSatisfies | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/d513fa8d76d13418049d8c27df6c2440332084b88c2561f90bee2cfce15dc169 | class=urn:codex:bootstrap:1.0.0#TraitExists | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/d96b5be3c3b1950d911dfe98d7a41926b8646ff0594a4e48ed175ef7d3b808a6 | class=urn:codex:bootstrap:1.0.0#ContentConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/dc637fc98d05b079818898ce0b868c47ba8a7c946851d4fe492320772468ddd3 | class=urn:codex:bootstrap:1.0.0#ValueInNumericRange | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/e45f071809685f79d4f6f9bbe9809e0a45fa10477905769d7a13fff7dfc7ad10 | class=urn:codex:bootstrap:1.0.0#CollectionAllowsDuplicates | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/e6f3a77e00b7e43cc3fd086d672062ed416fb016b19e5854d9197f8d5ce4f1d8 | class=urn:codex:bootstrap:1.0.0#ValueLength | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/ecd7960f09fb061cda24e8997f49919e14545be8074977659b4e2926c4d3a226 | class=urn:codex:bootstrap:1.0.0#ChildConstraint | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/ed10ad9d560720be8722ea1ca1d0bc45d26592dd81883e5665b1098adc39d4e9 | class=urn:codex:bootstrap:1.0.0#ChildSatisfies | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/f1698a235d5d97b80ffd43e81afad4b15767feacb8916442622322da1459da8a | class=urn:codex:bootstrap:1.0.0#TraitEquals | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/f852682a462b515853bc77cf48975160401ee999bd940eecbe64905548618feb | class=urn:codex:bootstrap:1.0.0#OnPathForAll | max=1
- child | urn:codex:bootstrap:1.0.0#Rule#child/faa69cca183e34ba59b9f8e5764cc6992bf00f9619855a10ab03a6737430e7db | class=urn:codex:bootstrap:1.0.0#ValueIsOneOf | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## Schema

### shape: urn:codex:bootstrap:1.0.0#Schema#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Schema
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#Schema#shape/xone/mode/203f7b982ddb4fde8ad183d93203879b2fd3a69e7f2db950f71c93106591fc63 | urn:codex:bootstrap:1.0.0#Schema#shape/xone/mode/0d457bf4834448d1f3099694cbbc8107a0f5b561c10ff63c018f76aa8cba248a
- child | urn:codex:bootstrap:1.0.0#Schema#child/2273e9a8c16630731662ad9fc73ac59a8b813e43c86addffaa7a79e52ce4de76 | class=urn:codex:bootstrap:1.0.0#ConceptDefinitions | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/3fdab872893285c4a884cb7b529be9302027284d5294884d6ba4ac63dca7dabc | class=urn:codex:bootstrap:1.0.0#EnumeratedValueSets | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/3ff6a188ac0e2fb50e9541e7c0cac2725e962a6a1a8e4e8e7d65bc56040b870a | class=urn:codex:bootstrap:1.0.0#ConstraintDefinitions | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/44c1517478a6e252b9e9b9d50edf62ac14d0ec4f48ee8a321bc6f6c9de89921d | class=urn:codex:bootstrap:1.0.0#SchemaImports | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/45973746b087585d62f22f8a63962f64afc5470b09833d68c8f039ae4b9539df | class=urn:codex:bootstrap:1.0.0#RdfGraph | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/575b76df24e95160f8544b57a14223f894ac19772f991354d4831d056151b8d2 | class=urn:codex:bootstrap:1.0.0#ValueTypeDefinitions | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/750999676b54773833ce69fcfffc830a87211a9a47cb3fa47fb651c5ba9a2c80 | class=urn:codex:bootstrap:1.0.0#ValidatorDefinitions | max=1
- child | urn:codex:bootstrap:1.0.0#Schema#child/7629360badd7fffe3bcb342e2ae5007c633e8dc8276c25d98cb8a7f9538566f1 | class=urn:codex:bootstrap:1.0.0#TraitDefinitions | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/declaredId | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- trait | urn:codex:bootstrap:1.0.0#authoringMode | min=1 | max=1 | in=[$CanonicalMode | $SimplifiedMode]
- trait | urn:codex:bootstrap:1.0.0#compatibilityClass | min=1 | max=1 | in=[$BackwardCompatible | $Breaking | $ForwardCompatible | $Initial]
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#key | datatype=urn:cdx:value-type:LookupToken | max=1
- trait | urn:codex:bootstrap:1.0.0#namespace | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#title | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#version | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#versionScheme | min=1 | max=1 | in=[$DateYYYYMM | $DateYYYYMMDD | $Lexical | $Semver]

### shape: urn:codex:bootstrap:1.0.0#Schema#shape/xone/mode/0d457bf4834448d1f3099694cbbc8107a0f5b561c10ff63c018f76aa8cba248a (subshape)
- prop | urn:codex:bootstrap:1.0.0#Schema#child/2273e9a8c16630731662ad9fc73ac59a8b813e43c86addffaa7a79e52ce4de76 | max=0
- prop | urn:codex:bootstrap:1.0.0#Schema#child/3fdab872893285c4a884cb7b529be9302027284d5294884d6ba4ac63dca7dabc | max=0
- prop | urn:codex:bootstrap:1.0.0#Schema#child/3ff6a188ac0e2fb50e9541e7c0cac2725e962a6a1a8e4e8e7d65bc56040b870a | max=0
- prop | urn:codex:bootstrap:1.0.0#Schema#child/45973746b087585d62f22f8a63962f64afc5470b09833d68c8f039ae4b9539df | min=1
- prop | urn:codex:bootstrap:1.0.0#Schema#child/575b76df24e95160f8544b57a14223f894ac19772f991354d4831d056151b8d2 | max=0
- prop | urn:codex:bootstrap:1.0.0#Schema#child/750999676b54773833ce69fcfffc830a87211a9a47cb3fa47fb651c5ba9a2c80 | max=0
- prop | urn:codex:bootstrap:1.0.0#Schema#child/7629360badd7fffe3bcb342e2ae5007c633e8dc8276c25d98cb8a7f9538566f1 | max=0
- prop | urn:codex:bootstrap:1.0.0#authoringMode | hasValue=$CanonicalMode

### shape: urn:codex:bootstrap:1.0.0#Schema#shape/xone/mode/203f7b982ddb4fde8ad183d93203879b2fd3a69e7f2db950f71c93106591fc63 (subshape)
- prop | urn:codex:bootstrap:1.0.0#Schema#child/2273e9a8c16630731662ad9fc73ac59a8b813e43c86addffaa7a79e52ce4de76 | min=1
- prop | urn:codex:bootstrap:1.0.0#Schema#child/45973746b087585d62f22f8a63962f64afc5470b09833d68c8f039ae4b9539df | max=0
- prop | urn:codex:bootstrap:1.0.0#authoringMode | hasValue=$SimplifiedMode

## SchemaImport

### shape: urn:codex:bootstrap:1.0.0#SchemaImport#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#SchemaImport
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#namespace | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#reference | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## SchemaImports

### shape: urn:codex:bootstrap:1.0.0#SchemaImports#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#SchemaImports
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#SchemaImports#child/35b5cdac88dfa77dd5503129f4d134585dca9a0f13f6acfb64659ddfab4f4929 | class=urn:codex:bootstrap:1.0.0#SchemaImport | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## TargetConcept

### shape: urn:codex:bootstrap:1.0.0#TargetConcept#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TargetConcept
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#conceptSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## TargetContext

### shape: urn:codex:bootstrap:1.0.0#TargetContext#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TargetContext
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#contextSelector | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## Targets

### shape: urn:codex:bootstrap:1.0.0#Targets#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Targets
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#Targets#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#Targets#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- child | urn:codex:bootstrap:1.0.0#Targets#child/0816fc31013825ca5f409d08acdadb71fe1008d86ef3601a139abdbf8fb16ba9 | class=urn:codex:bootstrap:1.0.0#TargetContext
- child | urn:codex:bootstrap:1.0.0#Targets#child/384b873ce59b888c39ded991e54f84c4bb370e10de12fd476b047216b7da7e11 | class=urn:codex:bootstrap:1.0.0#TargetConcept
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

### shape: urn:codex:bootstrap:1.0.0#Targets#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#Targets#child/384b873ce59b888c39ded991e54f84c4bb370e10de12fd476b047216b7da7e11 | min=1

### shape: urn:codex:bootstrap:1.0.0#Targets#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#Targets#child/0816fc31013825ca5f409d08acdadb71fe1008d86ef3601a139abdbf8fb16ba9 | min=1

## Then

### shape: urn:codex:bootstrap:1.0.0#Then#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#Then
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#Then#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## TraitCardinality

### shape: urn:codex:bootstrap:1.0.0#TraitCardinality#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitCardinality
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#TraitCardinality#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#TraitCardinality#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

### shape: urn:codex:bootstrap:1.0.0#TraitCardinality#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#min | min=1

### shape: urn:codex:bootstrap:1.0.0#TraitCardinality#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#max | min=1

## TraitDefinition

### shape: urn:codex:bootstrap:1.0.0#TraitDefinition#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitDefinition
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- xone: urn:codex:bootstrap:1.0.0#TraitDefinition#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 | urn:codex:bootstrap:1.0.0#TraitDefinition#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1
- child | urn:codex:bootstrap:1.0.0#TraitDefinition#child/0bd62a15e6910a4096a63e5b01ba0456f59ed50a4c727662f3ddb1e2117380a7 | class=urn:codex:bootstrap:1.0.0#AllowedValues
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#defaultValueType | datatype=urn:cdx:value-type:ValueTypeExpression | max=1
- trait | urn:codex:bootstrap:1.0.0#defaultValueTypes | datatype=urn:cdx:value-type:ValueTypeExpression | max=1
- trait | urn:codex:bootstrap:1.0.0#description | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#isReferenceTrait | datatype=http://www.w3.org/2001/XMLSchema#boolean | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#priority | max=1

### shape: urn:codex:bootstrap:1.0.0#TraitDefinition#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#defaultValueType | min=1
- prop | urn:codex:bootstrap:1.0.0#defaultValueTypes | max=0

### shape: urn:codex:bootstrap:1.0.0#TraitDefinition#shape/xone/ff2cd5be0c0f2b764740713cbcb7f23894b6cf398dd418cdbc7ce2fd56d2aca6/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#defaultValueType | max=0
- prop | urn:codex:bootstrap:1.0.0#defaultValueTypes | min=1

## TraitDefinitions

### shape: urn:codex:bootstrap:1.0.0#TraitDefinitions#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitDefinitions
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#TraitDefinitions#child/db72c9d9ff237dcdf1eb95e945cda26c2e00da4fd7290057488b414f92d8bbce | class=urn:codex:bootstrap:1.0.0#TraitDefinition | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## TraitEquals

### shape: urn:codex:bootstrap:1.0.0#TraitEquals#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitEquals
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#value | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## TraitExists

### shape: urn:codex:bootstrap:1.0.0#TraitExists#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitExists
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## TraitLessOrEqual

### shape: urn:codex:bootstrap:1.0.0#TraitLessOrEqual#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitLessOrEqual
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#leftTrait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#rightTrait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## TraitMissing

### shape: urn:codex:bootstrap:1.0.0#TraitMissing#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitMissing
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## TraitPath

### shape: urn:codex:bootstrap:1.0.0#TraitPath#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitPath
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#traitName | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## TraitRules

### shape: urn:codex:bootstrap:1.0.0#TraitRules#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitRules
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 | urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/2
- child | urn:codex:bootstrap:1.0.0#TraitRules#child/02340bdf69b8a5146182c5baa59d2f924509090ec1f951f6cb63c6f1628e91e4 | class=urn:codex:bootstrap:1.0.0#AllowsTrait
- child | urn:codex:bootstrap:1.0.0#TraitRules#child/025d8d45fd5dabf9599fc2b4e8aecfa1e9b81bff3c554475e8d7cc5a269d58ae | class=urn:codex:bootstrap:1.0.0#RequiresTrait
- child | urn:codex:bootstrap:1.0.0#TraitRules#child/e3d6faa4a9c2110974382fb0555ec03bf509eb57d80d06ba5516b1b5a910fc87 | class=urn:codex:bootstrap:1.0.0#ForbidsTrait
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

### shape: urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#TraitRules#child/025d8d45fd5dabf9599fc2b4e8aecfa1e9b81bff3c554475e8d7cc5a269d58ae | min=1

### shape: urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#TraitRules#child/02340bdf69b8a5146182c5baa59d2f924509090ec1f951f6cb63c6f1628e91e4 | min=1

### shape: urn:codex:bootstrap:1.0.0#TraitRules#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/2 (subshape)
- prop | urn:codex:bootstrap:1.0.0#TraitRules#child/e3d6faa4a9c2110974382fb0555ec03bf509eb57d80d06ba5516b1b5a910fc87 | min=1

## TraitValueType

### shape: urn:codex:bootstrap:1.0.0#TraitValueType#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#TraitValueType
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#valueType | datatype=urn:cdx:value-type:ValueTypeExpression | min=1 | max=1

## UniqueConstraint

### shape: urn:codex:bootstrap:1.0.0#UniqueConstraint#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#UniqueConstraint
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#scope | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#trait | datatype=urn:cdx:value-type:TraitName | min=1 | max=1

## ValidatorDefinition

### shape: urn:codex:bootstrap:1.0.0#ValidatorDefinition#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValidatorDefinition
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/content | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#message | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=urn:cdx:value-type:ConceptName | min=1 | max=1

## ValidatorDefinitions

### shape: urn:codex:bootstrap:1.0.0#ValidatorDefinitions#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValidatorDefinitions
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ValidatorDefinitions#child/3a49ad950eaef09a4a6abe794aba860c1666bc949e5c488b226f47fa0a14ee27 | class=urn:codex:bootstrap:1.0.0#ValidatorDefinition | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ValueInNumericRange

### shape: urn:codex:bootstrap:1.0.0#ValueInNumericRange#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueInNumericRange
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#ValueInNumericRange#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#ValueInNumericRange#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#decimal | max=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#decimal | max=1

### shape: urn:codex:bootstrap:1.0.0#ValueInNumericRange#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#min | min=1

### shape: urn:codex:bootstrap:1.0.0#ValueInNumericRange#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#max | min=1

## ValueIsNonEmpty

### shape: urn:codex:bootstrap:1.0.0#ValueIsNonEmpty#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueIsNonEmpty
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## ValueIsOneOf

### shape: urn:codex:bootstrap:1.0.0#ValueIsOneOf#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueIsOneOf
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#values | datatype=urn:cdx:value-type:ValueExpression | min=1 | max=1

## ValueIsValid

### shape: urn:codex:bootstrap:1.0.0#ValueIsValid#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueIsValid
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#validatorName | min=1 | max=1

## ValueLength

### shape: urn:codex:bootstrap:1.0.0#ValueLength#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueLength
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- or: urn:codex:bootstrap:1.0.0#ValueLength#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 | urn:codex:bootstrap:1.0.0#ValueLength#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#max | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1
- trait | urn:codex:bootstrap:1.0.0#min | datatype=http://www.w3.org/2001/XMLSchema#integer | max=1

### shape: urn:codex:bootstrap:1.0.0#ValueLength#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/0 (subshape)
- prop | urn:codex:bootstrap:1.0.0#min | min=1

### shape: urn:codex:bootstrap:1.0.0#ValueLength#shape/or/37d682d06b98556f4eeab841011a9e2e0554d6547504a0179606946fdc560efc/shape/1 (subshape)
- prop | urn:codex:bootstrap:1.0.0#max | min=1

## ValueMatchesPattern

### shape: urn:codex:bootstrap:1.0.0#ValueMatchesPattern#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueMatchesPattern
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#flags | datatype=http://www.w3.org/2001/XMLSchema#string | max=1
- trait | urn:codex:bootstrap:1.0.0#pattern | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1

## ValueTypeDefinition

### shape: urn:codex:bootstrap:1.0.0#ValueTypeDefinition#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueTypeDefinition
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=true
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#baseValueType | datatype=urn:cdx:value-type:ValueTypeExpression | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#name | datatype=http://www.w3.org/2001/XMLSchema#string | min=1 | max=1
- trait | urn:codex:bootstrap:1.0.0#validatorName | max=1

## ValueTypeDefinitions

### shape: urn:codex:bootstrap:1.0.0#ValueTypeDefinitions#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#ValueTypeDefinitions
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#ValueTypeDefinitions#child/dd9dceb8fad39c12589f87d7aff8da2818cee6b90fa57340731791f53467a1fb | class=urn:codex:bootstrap:1.0.0#ValueTypeDefinition | min=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

## When

### shape: urn:codex:bootstrap:1.0.0#When#shape (root)
- targetClass: urn:codex:bootstrap:1.0.0#When
- closed: true
- ignoredProperties: http://www.w3.org/1999/02/22-rdf-syntax-ns#type | urn:codex:bootstrap:1.0.0#codex/content | urn:codex:bootstrap:1.0.0#codex/declaredId | urn:codex:bootstrap:1.0.0#codex/isEntity | urn:codex:bootstrap:1.0.0#codex/parentNode
- child | urn:codex:bootstrap:1.0.0#When#child/1f1ee75c20d9e8bf4a33feea2915f6b88f24b21e995c0860033130c785d4b9f2 | class=urn:codex:bootstrap:1.0.0#Rule | min=1 | max=1
- predicate | urn:codex:bootstrap:1.0.0#codex/isEntity | datatype=http://www.w3.org/2001/XMLSchema#boolean | min=1 | max=1 | hasValue=false
- predicate | urn:codex:bootstrap:1.0.0#codex/parentNode | nodeKind=http://www.w3.org/ns/shacl#IRI | min=1 | max=1

