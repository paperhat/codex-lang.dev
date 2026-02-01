# Behavior Type System

This document specifies the complete type system for Behavior expressions including all operators, their signatures, and type rules.

---

## 1. Value Model

### 1.1 Scalar Types

| Type | Description |
|------|-------------|
| `Boolean` | `true` or `false` |
| `Text` | Sequence of Unicode scalar values |
| `Character` | Single Unicode scalar value |

### 1.2 Numeric Types

| Type | Description |
|------|-------------|
| `Integer` | Exact integer (unbounded) |
| `Zero` | The integer zero (`0`) |
| `NegativeInteger` | Integer with a `-` sign (digits are not `0`) |
| `NonPositiveInteger` | `Zero` or `NegativeInteger` |
| `NonNegativeInteger` | `Zero` or `PositiveInteger` |
| `PositiveInteger` | Integer with no `-` sign (digits are not `0`) |
| `DecimalNumber` | Number with decimal point (`3.14`) |
| `ExponentialNumber` | Number with exponent (`3.14e10`) |
| `PrecisionNumber` | Decimal with explicit precision (`3.14p2`) |
| `Fraction` | Exact rational (`3/4`) |
| `ImaginaryNumber` | Pure imaginary (`2i`) |
| `ComplexNumber` | Real + imaginary (`2+3i`) |
| `PositiveInfinity` | Positive infinity (`Infinity`) |
| `NegativeInfinity` | Negative infinity (`-Infinity`) |
| `Infinity` | `Infinity` or `-Infinity` |

**Special Values:** `Infinity`, `-Infinity` (NaN is prohibited per Codex §5.4; integer `-0` is invalid)

### 1.3 Derived Numeric Domains

| Domain | Definition |
|--------|------------|
| `OrderableNumber` | Integer \| Fraction \| PrecisionNumber |
| `OrderableRealNumber` | OrderableNumber \| Infinity |
| `ExactNumber` | Integer \| Fraction |
| `AnyRealNumber` | Integer \| DecimalNumber \| ExponentialNumber \| PrecisionNumber \| Fraction \| Infinity |
| `AnyNumber` | AnyRealNumber \| ImaginaryNumber \| ComplexNumber |

### 1.4 Collection Types

| Type | Description |
|------|-------------|
| `List<T>` | Ordered sequence, duplicates allowed |
| `Set<T>` | Unordered collection, unique elements |
| `Tuple<T1, T2, ...>` | Fixed-length, positional |
| `Map<K, V>` | Key-value pairs (keys: Text, Character, Integer, EnumeratedToken) |
| `Record<V>` | Text-keyed Map (equivalent to `Map<Text, V>`) |
| `Range<T>` | Declarative interval (common: numeric, temporal, character, text; other semantics schema-defined) |

**Unparameterized collection types accept values of any type.** When a schema specifies `$List` without a type parameter, the list may contain values of any type. To constrain element types, use the parameterized form (e.g., `$List<Integer>`).

### 1.5 Temporal Types

Temporal Values are spelled as `{...}` in Codex surface form and are first recognized and classified syntactically (per the spec’s Temporal Body grammar).

At the semantic layer (schema validation), when a governing schema expects a temporal value type (e.g., `$PlainDate`, `$Instant`), the implementation must convert the parsed temporal spelling into a corresponding semantic temporal value (i.e., a concrete runtime type in the reference implementation). If conversion fails, validation must fail with a `SchemaError`.

`{now}` and `{today}` are a special case: they must be represented as **unevaluated** `TemporalKeyword` values and must not be converted to an `Instant` or `PlainDate` during validation or evaluation. Their meaning is resolved only when a consuming system explicitly renders or otherwise interprets them.

If a schema expects a deterministic temporal type (e.g., `$Instant`, `$PlainDate`) and the provided value is a `TemporalKeyword`, validation must fail with a `SchemaError` unless the schema explicitly permits `$TemporalKeyword` (or `$Temporal`) at that location.

Canonical surface form still preserves the original parsed spelling; semantic conversion is for validation and evaluation, not for rewriting the source spelling.

**Derived temporal domains**

| Domain | Definition |
|--------|------------|
| `DeterministicTemporal` | PlainDate \| PlainTime \| PlainDateTime \| PlainYearMonth \| PlainMonthDay \| YearWeek \| Instant \| ZonedDateTime \| Duration |
| `Temporal` | DeterministicTemporal \| TemporalKeyword |

| Type | Description |
|------|-------------|
| `PlainDate` | Calendar date without time or timezone |
| `PlainTime` | Wall-clock time without date or timezone |
| `PlainDateTime` | Date and time without timezone |
| `PlainYearMonth` | Year and month |
| `PlainMonthDay` | Month and day |
| `YearWeek` | ISO year and week number |
| `Instant` | Absolute point in time (UTC) |
| `ZonedDateTime` | Date, time, and timezone |
| `Duration` | Length of time |
| `TimeZone` | IANA timezone identifier |
| `Calendar` | Calendar system identifier |

### 1.6 Color Types

| Type | Description |
|------|-------------|
| `HexColor` | Hexadecimal color (`#RGB`, `#RRGGBB`, etc.) |
| `NamedColor` | Named color (`&red`, `&blue`, etc.) |
| `RgbColor` | RGB color function |
| `HslColor` | HSL color function |
| `HwbColor` | HWB color function |
| `LabColor` | CIE Lab color function |
| `LchColor` | CIE LCH color function |
| `OklabColor` | Oklab color function |
| `OklchColor` | Oklch color function |
| `ColorFunction` | Generic `color()` function |
| `ColorMix` | `color-mix()` function |
| `DeviceCmyk` | `device-cmyk()` function |

Semantic validity rules for perceptual color functions (Lab/LCH and OKLab/OKLCH), including the deterministic conversion-based in-gamut check and mandated numeric requirements, are specified normatively in [spec/1.0.0/index.md](../../spec/1.0.0/index.md#572-deterministic-conversion-based-validity-lablch-oklaboklch).

### 1.7 Identity Types

| Type | Description |
|------|-------------|
| `Uuid` | RFC 4122 UUID |
| `IriReference` | Internationalized Resource Identifier |
| `LookupToken` | Document-scoped reference |
| `EnumeratedToken` | Schema-defined token |
| `HostName` | Host name wrapper value (canonicalized) |
| `EmailAddress` | Email address wrapper value (canonicalized) |
| `Url` | URL wrapper value (canonicalized) |

### 1.8 Missingness

| Type | Description |
|------|-------------|
| `Absent` | Canonical missing value (distinct from empty collections) |

---

## 2. Evaluation Model

All evaluation produces `Validation<T>`:
- `Valid(value)` — successful evaluation
- `Invalid(diagnostics)` — evaluation failed with error information

Evaluators return `Invalid(...)` rather than throwing exceptions.

---

## 3. Type Checking Rules

1. Operators receiving values outside their domain return `Invalid([...])`
2. Coercion is explicit (via vocabulary operators) unless an operator defines fixed coercion
3. No implicit coercion between unrelated domains

### 3.1 Numeric Promotion

| Combination | Result |
|-------------|--------|
| Integer + Fraction | Fraction |
| Integer + PrecisionNumber | PrecisionNumber |
| Fraction + PrecisionNumber | PrecisionNumber |
| Any exact + DecimalNumber | DecimalNumber |
| Any real + ImaginaryNumber | ComplexNumber |
| Any real + ComplexNumber | ComplexNumber |

---

## 4. Mathematical Operators

### 4.1 Constants

| Operator | Result Type | Description |
|----------|-------------|-------------|
| `Pi` | DecimalNumber | π ≈ 3.14159265358979 |
| `E` | DecimalNumber | Euler's number ≈ 2.71828182845905 |
| `GoldenRatio` | DecimalNumber | φ ≈ 1.61803398874989 |
| `EulerMascheroni` | DecimalNumber | γ ≈ 0.57721566490153 |

### 4.2 Basic Arithmetic

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Add` | `(AnyNumber, AnyNumber, ...) → AnyNumber` | Sum of operands |
| `Subtract` | `(AnyNumber, AnyNumber) → AnyNumber` | Difference |
| `Multiply` | `(AnyNumber, AnyNumber, ...) → AnyNumber` | Product of operands |
| `DivideBy` | `(AnyNumber, AnyNumber) → AnyNumber` | Division |
| `Negate` | `(AnyNumber) → AnyNumber` | Negation |
| `AbsoluteValue` | `(AnyNumber) → AnyRealNumber` | Absolute value |
| `Sign` | `(AnyRealNumber) → Integer` | -1, 0, or 1 |
| `Reciprocal` | `(AnyNumber) → AnyNumber` | 1/x |

### 4.3 Integer Arithmetic

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IntegerDivideBy` | `(Integer, Integer) → Integer` | Integer division (truncated) |
| `Modulo` | `(Integer, Integer) → Integer` | Remainder |
| `FlooredDivideBy` | `(Integer, Integer) → Integer` | Floor division |
| `FlooredModulo` | `(Integer, Integer) → Integer` | Floor remainder |
| `EuclideanDivideBy` | `(Integer, Integer) → Integer` | Euclidean division |
| `EuclideanModulo` | `(Integer, Integer) → Integer` | Euclidean remainder |
| `DivideWithRemainder` | `(Integer, Integer) → Tuple<Integer, Integer>` | Quotient and remainder |

### 4.4 Complex Number Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ComplexFromPolar` | `(AnyRealNumber, AnyRealNumber) → ComplexNumber` | From magnitude and angle |
| `RealPart` | `(ComplexNumber) → AnyRealNumber` | Real component |
| `ImaginaryPart` | `(ComplexNumber) → AnyRealNumber` | Imaginary component |
| `Magnitude` | `(ComplexNumber) → AnyRealNumber` | Absolute value |
| `Phase` | `(ComplexNumber) → AnyRealNumber` | Angle in radians |
| `Conjugate` | `(ComplexNumber) → ComplexNumber` | Complex conjugate |

### 4.5 Value Bounds

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Minimum` | `(OrderableRealNumber, OrderableRealNumber, ...) → OrderableRealNumber` | Smallest value |
| `Maximum` | `(OrderableRealNumber, OrderableRealNumber, ...) → OrderableRealNumber` | Largest value |
| `Clamp` | `(OrderableRealNumber, OrderableRealNumber, OrderableRealNumber) → OrderableRealNumber` | Constrain to range |

### 4.6 Rounding

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Round` | `(AnyRealNumber) → Integer` | Round half away from zero |
| `RoundHalfEven` | `(AnyRealNumber) → Integer` | Round half to even (banker's) |
| `RoundHalfUp` | `(AnyRealNumber) → Integer` | Round half up |
| `RoundHalfDown` | `(AnyRealNumber) → Integer` | Round half down |
| `RoundTowardZero` | `(AnyRealNumber) → Integer` | Truncate toward zero |
| `RoundAwayFromZero` | `(AnyRealNumber) → Integer` | Round away from zero |
| `Floor` | `(AnyRealNumber) → Integer` | Round toward -∞ |
| `Ceiling` | `(AnyRealNumber) → Integer` | Round toward +∞ |
| `RoundToPlaces` | `(AnyRealNumber, Integer) → PrecisionNumber` | Round to decimal places |
| `RoundToSignificantFigures` | `(AnyRealNumber, Integer) → PrecisionNumber` | Round to sig figs |

### 4.7 Powers, Roots, and Logarithms

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Power` | `(AnyNumber, AnyNumber) → AnyNumber` | Exponentiation |
| `SquareRoot` | `(AnyNumber) → AnyNumber` | Square root |
| `CubeRoot` | `(AnyRealNumber) → AnyRealNumber` | Cube root |
| `NthRoot` | `(AnyNumber, Integer) → AnyNumber` | nth root |
| `Exponential` | `(AnyNumber) → AnyNumber` | e^x |
| `NaturalLogarithm` | `(AnyNumber) → AnyNumber` | ln(x) |
| `LogarithmBase10` | `(AnyNumber) → AnyNumber` | log₁₀(x) |
| `LogarithmBase2` | `(AnyNumber) → AnyNumber` | log₂(x) |
| `Logarithm` | `(AnyNumber, AnyNumber) → AnyNumber` | logₐ(x) |
| `Expm1` | `(AnyRealNumber) → AnyRealNumber` | e^x - 1 (precise for small x) |
| `Log1p` | `(AnyRealNumber) → AnyRealNumber` | ln(1+x) (precise for small x) |

### 4.8 Trigonometry

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Sine` | `(AnyNumber) → AnyNumber` | sin(x), x in radians |
| `Cosine` | `(AnyNumber) → AnyNumber` | cos(x), x in radians |
| `Tangent` | `(AnyNumber) → AnyNumber` | tan(x), x in radians |
| `Cotangent` | `(AnyNumber) → AnyNumber` | cot(x), x in radians |
| `Secant` | `(AnyNumber) → AnyNumber` | sec(x), x in radians |
| `Cosecant` | `(AnyNumber) → AnyNumber` | csc(x), x in radians |
| `ArcSine` | `(AnyNumber) → AnyNumber` | arcsin(x) in radians |
| `ArcCosine` | `(AnyNumber) → AnyNumber` | arccos(x) in radians |
| `ArcTangent` | `(AnyNumber) → AnyNumber` | arctan(x) in radians |
| `ArcTangent2` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | atan2(y, x) |
| `ArcCotangent` | `(AnyNumber) → AnyNumber` | arccot(x) |
| `ArcSecant` | `(AnyNumber) → AnyNumber` | arcsec(x) |
| `ArcCosecant` | `(AnyNumber) → AnyNumber` | arccsc(x) |
| `DegreesToRadians` | `(AnyRealNumber) → AnyRealNumber` | Convert degrees to radians |
| `RadiansToDegrees` | `(AnyRealNumber) → AnyRealNumber` | Convert radians to degrees |
| `Sinc` | `(AnyRealNumber) → AnyRealNumber` | sin(x)/x (1 at x=0) |
| `Haversine` | `(AnyRealNumber) → AnyRealNumber` | (1 - cos(x))/2 |

### 4.9 Hyperbolic Functions

| Operator | Signature | Description |
|----------|-----------|-------------|
| `HyperbolicSine` | `(AnyNumber) → AnyNumber` | sinh(x) |
| `HyperbolicCosine` | `(AnyNumber) → AnyNumber` | cosh(x) |
| `HyperbolicTangent` | `(AnyNumber) → AnyNumber` | tanh(x) |
| `HyperbolicCotangent` | `(AnyNumber) → AnyNumber` | coth(x) |
| `HyperbolicSecant` | `(AnyNumber) → AnyNumber` | sech(x) |
| `HyperbolicCosecant` | `(AnyNumber) → AnyNumber` | csch(x) |
| `InverseHyperbolicSine` | `(AnyNumber) → AnyNumber` | asinh(x) |
| `InverseHyperbolicCosine` | `(AnyNumber) → AnyNumber` | acosh(x) |
| `InverseHyperbolicTangent` | `(AnyNumber) → AnyNumber` | atanh(x) |
| `InverseHyperbolicCotangent` | `(AnyNumber) → AnyNumber` | acoth(x) |
| `InverseHyperbolicSecant` | `(AnyNumber) → AnyNumber` | asech(x) |
| `InverseHyperbolicCosecant` | `(AnyNumber) → AnyNumber` | acsch(x) |

### 4.10 Statistics

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Sum` | `(List<AnyNumber>) → AnyNumber` | Sum of elements |
| `Product` | `(List<AnyNumber>) → AnyNumber` | Product of elements |
| `ArithmeticMean` | `(List<AnyNumber>) → AnyRealNumber` | Average |
| `GeometricMean` | `(List<AnyRealNumber>) → AnyRealNumber` | Geometric average |
| `HarmonicMean` | `(List<AnyRealNumber>) → AnyRealNumber` | Harmonic average |
| `Median` | `(List<OrderableRealNumber>) → OrderableRealNumber` | Middle value |
| `Mode` | `(List<T>) → List<T>` | Most frequent value(s) |
| `Variance` | `(List<AnyNumber>) → AnyRealNumber` | Population variance |
| `SampleVariance` | `(List<AnyNumber>) → AnyRealNumber` | Sample variance |
| `StandardDeviation` | `(List<AnyNumber>) → AnyRealNumber` | Population std dev |
| `SampleStandardDeviation` | `(List<AnyNumber>) → AnyRealNumber` | Sample std dev |
| `Covariance` | `(List<AnyNumber>, List<AnyNumber>) → AnyRealNumber` | Population covariance |
| `SampleCovariance` | `(List<AnyNumber>, List<AnyNumber>) → AnyRealNumber` | Sample covariance |
| `PearsonCorrelation` | `(List<AnyNumber>, List<AnyNumber>) → AnyRealNumber` | Pearson r |
| `SpearmanCorrelation` | `(List<OrderableRealNumber>, List<OrderableRealNumber>) → AnyRealNumber` | Spearman ρ |
| `Percentile` | `(List<OrderableRealNumber>, AnyRealNumber) → OrderableRealNumber` | Percentile value |
| `Quantile` | `(List<OrderableRealNumber>, AnyRealNumber) → OrderableRealNumber` | Quantile value |
| `InterquartileRange` | `(List<OrderableRealNumber>) → OrderableRealNumber` | IQR |
| `MeanAbsoluteDeviation` | `(List<AnyNumber>) → AnyRealNumber` | MAD |
| `RootMeanSquare` | `(List<AnyNumber>) → AnyRealNumber` | RMS |
| `Skewness` | `(List<AnyNumber>) → AnyRealNumber` | Distribution skewness |
| `Kurtosis` | `(List<AnyNumber>) → AnyRealNumber` | Distribution kurtosis |
| `ZScore` | `(AnyNumber, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Standard score |

### 4.11 Combinatorics

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Factorial` | `(Integer) → Integer` | n! |
| `DoubleFactorial` | `(Integer) → Integer` | n!! |
| `BinomialCoefficient` | `(Integer, Integer) → Integer` | C(n,k) |
| `Permutations` | `(Integer, Integer) → Integer` | P(n,k) |
| `Multinomial` | `(List<Integer>) → Integer` | Multinomial coefficient |
| `CatalanNumber` | `(Integer) → Integer` | nth Catalan number |
| `FibonacciNumber` | `(Integer) → Integer` | nth Fibonacci number |
| `LucasNumber` | `(Integer) → Integer` | nth Lucas number |
| `StirlingFirst` | `(Integer, Integer) → Integer` | Stirling number 1st kind |
| `StirlingSecond` | `(Integer, Integer) → Integer` | Stirling number 2nd kind |
| `BellNumber` | `(Integer) → Integer` | nth Bell number |
| `PartitionCount` | `(Integer) → Integer` | Integer partition count |

### 4.12 Number Theory

| Operator | Signature | Description |
|----------|-----------|-------------|
| `GreatestCommonDivisor` | `(Integer, Integer, ...) → Integer` | GCD |
| `LeastCommonMultiple` | `(Integer, Integer, ...) → Integer` | LCM |
| `ExtendedGcd` | `(Integer, Integer) → Tuple<Integer, Integer, Integer>` | GCD with Bézout coefficients |
| `IsPrime` | `(Integer) → Boolean` | Primality test |
| `PrimeFactorization` | `(Integer) → List<Tuple<Integer, Integer>>` | Prime factors with exponents |
| `Divisors` | `(Integer) → List<Integer>` | All divisors |
| `DivisorCount` | `(Integer) → Integer` | τ(n) |
| `DivisorSum` | `(Integer) → Integer` | σ(n) |
| `EulerTotient` | `(Integer) → Integer` | φ(n) |
| `MoebiusFunction` | `(Integer) → Integer` | μ(n) |
| `LiouvilleFunction` | `(Integer) → Integer` | λ(n) |
| `ModularExponentiation` | `(Integer, Integer, Integer) → Integer` | a^b mod m |
| `ModularInverse` | `(Integer, Integer) → Integer` | a⁻¹ mod m |
| `ChineseRemainderTheorem` | `(List<Integer>, List<Integer>) → Integer` | CRT solution |

### 4.13 Linear Algebra

| Operator | Signature | Description |
|----------|-----------|-------------|
| `DotProduct` | `(List<AnyNumber>, List<AnyNumber>) → AnyNumber` | Inner product |
| `CrossProduct` | `(List<AnyNumber>, List<AnyNumber>) → List<AnyNumber>` | Cross product (3D) |
| `VectorNorm` | `(List<AnyNumber>) → AnyRealNumber` | Euclidean norm |
| `VectorNormP` | `(List<AnyNumber>, AnyRealNumber) → AnyRealNumber` | p-norm |
| `VectorNormInfinity` | `(List<AnyNumber>) → AnyRealNumber` | Infinity norm |
| `NormalizeVector` | `(List<AnyNumber>) → List<AnyRealNumber>` | Unit vector |
| `MatrixAdd` | `(List<List<AnyNumber>>, List<List<AnyNumber>>) → List<List<AnyNumber>>` | Matrix addition |
| `MatrixSubtract` | `(List<List<AnyNumber>>, List<List<AnyNumber>>) → List<List<AnyNumber>>` | Matrix subtraction |
| `MatrixMultiply` | `(List<List<AnyNumber>>, List<List<AnyNumber>>) → List<List<AnyNumber>>` | Matrix multiplication |
| `MatrixScalarMultiply` | `(List<List<AnyNumber>>, AnyNumber) → List<List<AnyNumber>>` | Scalar multiplication |
| `MatrixTranspose` | `(List<List<AnyNumber>>) → List<List<AnyNumber>>` | Transpose |
| `MatrixDeterminant` | `(List<List<AnyNumber>>) → AnyNumber` | Determinant |
| `MatrixInverse` | `(List<List<AnyNumber>>) → List<List<AnyNumber>>` | Inverse |
| `MatrixTrace` | `(List<List<AnyNumber>>) → AnyNumber` | Trace |
| `MatrixRank` | `(List<List<AnyNumber>>) → Integer` | Rank |
| `IdentityMatrix` | `(Integer) → List<List<Integer>>` | n×n identity matrix |
| `ZeroMatrix` | `(Integer, Integer) → List<List<Integer>>` | m×n zero matrix |
| `MatrixRowEchelon` | `(List<List<AnyNumber>>) → List<List<AnyNumber>>` | Row echelon form |
| `MatrixReducedRowEchelon` | `(List<List<AnyNumber>>) → List<List<AnyNumber>>` | Reduced row echelon |
| `SolveLinearSystem` | `(List<List<AnyNumber>>, List<AnyNumber>) → List<AnyNumber>` | Solve Ax = b |
| `Eigenvalues` | `(List<List<AnyNumber>>) → List<AnyNumber>` | Eigenvalues |
| `Eigenvectors` | `(List<List<AnyNumber>>) → List<List<AnyNumber>>` | Eigenvectors |

### 4.14 Calculus

| Operator | Signature | Description |
|----------|-----------|-------------|
| `NumericalDerivative` | `(Expression, Text, AnyRealNumber) → AnyRealNumber` | Derivative at point |
| `NumericalSecondDerivative` | `(Expression, Text, AnyRealNumber) → AnyRealNumber` | Second derivative |
| `NumericalPartialDerivative` | `(Expression, Text, Map<Text, AnyRealNumber>) → AnyRealNumber` | Partial derivative |
| `NumericalGradient` | `(Expression, List<Text>, Map<Text, AnyRealNumber>) → List<AnyRealNumber>` | Gradient vector |
| `NumericalIntegral` | `(Expression, Text, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Definite integral |
| `NumericalDoubleIntegral` | `(Expression, Text, AnyRealNumber, AnyRealNumber, Text, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Double integral |
| `FindRoot` | `(Expression, Text, AnyRealNumber) → AnyRealNumber` | Root finding |
| `FindAllRoots` | `(Expression, Text, AnyRealNumber, AnyRealNumber) → List<AnyRealNumber>` | All roots in interval |
| `FindMinimum` | `(Expression, Text, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Minimum in interval |
| `FindMaximum` | `(Expression, Text, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Maximum in interval |
| `TaylorSeries` | `(Expression, Text, AnyRealNumber, Integer) → List<AnyRealNumber>` | Taylor coefficients |
| `Limit` | `(Expression, Text, AnyRealNumber) → AnyRealNumber` | Limit at point |

### 4.15 Special Functions

| Operator | Signature | Description |
|----------|-----------|-------------|
| `GammaFunction` | `(AnyNumber) → AnyNumber` | Γ(x) |
| `LogGammaFunction` | `(AnyNumber) → AnyNumber` | ln(Γ(x)) |
| `DigammaFunction` | `(AnyNumber) → AnyNumber` | ψ(x) = Γ'(x)/Γ(x) |
| `BetaFunction` | `(AnyNumber, AnyNumber) → AnyNumber` | B(a,b) |
| `IncompleteBetaFunction` | `(AnyRealNumber, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Iₓ(a,b) |
| `IncompleteGammaFunction` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | γ(s,x) |
| `ErrorFunction` | `(AnyNumber) → AnyNumber` | erf(x) |
| `ComplementaryErrorFunction` | `(AnyNumber) → AnyNumber` | erfc(x) |
| `InverseErrorFunction` | `(AnyRealNumber) → AnyRealNumber` | erf⁻¹(x) |
| `BesselJ` | `(Integer, AnyNumber) → AnyNumber` | Bessel function 1st kind |
| `BesselY` | `(Integer, AnyNumber) → AnyNumber` | Bessel function 2nd kind |
| `BesselI` | `(Integer, AnyNumber) → AnyNumber` | Modified Bessel 1st kind |
| `BesselK` | `(Integer, AnyNumber) → AnyNumber` | Modified Bessel 2nd kind |
| `SphericalBesselJ` | `(Integer, AnyNumber) → AnyNumber` | Spherical Bessel 1st kind |
| `SphericalBesselY` | `(Integer, AnyNumber) → AnyNumber` | Spherical Bessel 2nd kind |
| `AiryAi` | `(AnyNumber) → AnyNumber` | Airy function Ai |
| `AiryBi` | `(AnyNumber) → AnyNumber` | Airy function Bi |
| `RiemannZeta` | `(AnyNumber) → AnyNumber` | ζ(s) |
| `HurwitzZeta` | `(AnyNumber, AnyNumber) → AnyNumber` | ζ(s,a) |
| `Polylogarithm` | `(Integer, AnyNumber) → AnyNumber` | Liₙ(z) |
| `LegendreP` | `(Integer, AnyNumber) → AnyNumber` | Legendre polynomial Pₙ |
| `AssociatedLegendreP` | `(Integer, Integer, AnyNumber) → AnyNumber` | Associated Legendre |
| `ChebyshevT` | `(Integer, AnyNumber) → AnyNumber` | Chebyshev 1st kind Tₙ |
| `ChebyshevU` | `(Integer, AnyNumber) → AnyNumber` | Chebyshev 2nd kind Uₙ |
| `HermiteH` | `(Integer, AnyNumber) → AnyNumber` | Hermite polynomial Hₙ |
| `LaguerreL` | `(Integer, AnyNumber) → AnyNumber` | Laguerre polynomial Lₙ |
| `AssociatedLaguerreL` | `(Integer, Integer, AnyNumber) → AnyNumber` | Associated Laguerre |
| `SphericalHarmonicY` | `(Integer, Integer, AnyRealNumber, AnyRealNumber) → ComplexNumber` | Yₗᵐ(θ,φ) |
| `EllipticK` | `(AnyNumber) → AnyNumber` | Complete elliptic integral K |
| `EllipticE` | `(AnyNumber) → AnyNumber` | Complete elliptic integral E |
| `EllipticF` | `(AnyNumber, AnyNumber) → AnyNumber` | Incomplete elliptic F |
| `EllipticPi` | `(AnyNumber, AnyNumber, AnyNumber) → AnyNumber` | Elliptic integral Π |
| `JacobiSn` | `(AnyNumber, AnyNumber) → AnyNumber` | Jacobi elliptic sn |
| `JacobiCn` | `(AnyNumber, AnyNumber) → AnyNumber` | Jacobi elliptic cn |
| `JacobiDn` | `(AnyNumber, AnyNumber) → AnyNumber` | Jacobi elliptic dn |

### 4.16 Interpolation

| Operator | Signature | Description |
|----------|-----------|-------------|
| `LinearInterpolate` | `(AnyRealNumber, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Lerp: a + t(b-a) |
| `BilinearInterpolate` | `(AnyRealNumber, AnyRealNumber, List<List<AnyRealNumber>>) → AnyRealNumber` | 2D interpolation |
| `CubicInterpolate` | `(List<AnyRealNumber>, List<AnyRealNumber>, AnyRealNumber) → AnyRealNumber` | Cubic spline |
| `LagrangeInterpolate` | `(List<AnyRealNumber>, List<AnyRealNumber>, AnyRealNumber) → AnyRealNumber` | Lagrange polynomial |
| `NewtonInterpolate` | `(List<AnyRealNumber>, List<AnyRealNumber>, AnyRealNumber) → AnyRealNumber` | Newton's divided differences |

### 4.17 Geometry 2D

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Point2D` | `(AnyRealNumber, AnyRealNumber) → Point2D` | Create 2D point |
| `DistanceBetweenPoints2D` | `(Point2D, Point2D) → AnyRealNumber` | Euclidean distance |
| `ManhattanDistance2D` | `(Point2D, Point2D) → AnyRealNumber` | Manhattan distance |
| `Midpoint2D` | `(Point2D, Point2D) → Point2D` | Midpoint |
| `AngleBetweenPoints2D` | `(Point2D, Point2D) → AnyRealNumber` | Angle in radians |
| `RotatePoint2D` | `(Point2D, AnyRealNumber, Point2D) → Point2D` | Rotate around center |
| `TranslatePoint2D` | `(Point2D, AnyRealNumber, AnyRealNumber) → Point2D` | Translate |
| `ScalePoint2D` | `(Point2D, AnyRealNumber, Point2D) → Point2D` | Scale from center |
| `ReflectPoint2D` | `(Point2D, Point2D, Point2D) → Point2D` | Reflect across line |
| `PointInRectangle` | `(Point2D, Point2D, Point2D) → Boolean` | Point containment |
| `PointInCircle` | `(Point2D, Point2D, AnyRealNumber) → Boolean` | Point containment |
| `PointInPolygon` | `(Point2D, List<Point2D>) → Boolean` | Point containment |
| `AreaOfTriangle2D` | `(Point2D, Point2D, Point2D) → AnyRealNumber` | Triangle area |
| `AreaOfPolygon` | `(List<Point2D>) → AnyRealNumber` | Polygon area |
| `PerimeterOfPolygon` | `(List<Point2D>) → AnyRealNumber` | Polygon perimeter |
| `CentroidOfPolygon` | `(List<Point2D>) → Point2D` | Polygon centroid |
| `ConvexHull` | `(List<Point2D>) → List<Point2D>` | Convex hull |
| `BoundingBox2D` | `(List<Point2D>) → Tuple<Point2D, Point2D>` | Bounding rectangle |
| `LineIntersection2D` | `(Point2D, Point2D, Point2D, Point2D) → Point2D \| Absent` | Line intersection |
| `SegmentIntersection2D` | `(Point2D, Point2D, Point2D, Point2D) → Point2D \| Absent` | Segment intersection |
| `PointToLineDistance2D` | `(Point2D, Point2D, Point2D) → AnyRealNumber` | Point-line distance |
| `PointToSegmentDistance2D` | `(Point2D, Point2D, Point2D) → AnyRealNumber` | Point-segment distance |
| `CircleArea` | `(AnyRealNumber) → AnyRealNumber` | πr² |
| `CircleCircumference` | `(AnyRealNumber) → AnyRealNumber` | 2πr |
| `ArcLength` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Arc length |
| `SectorArea` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Sector area |
| `ChordLength` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | Chord length |

### 4.18 Geometry 3D

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Point3D` | `(AnyRealNumber, AnyRealNumber, AnyRealNumber) → Point3D` | Create 3D point |
| `DistanceBetweenPoints3D` | `(Point3D, Point3D) → AnyRealNumber` | Euclidean distance |
| `ManhattanDistance3D` | `(Point3D, Point3D) → AnyRealNumber` | Manhattan distance |
| `Midpoint3D` | `(Point3D, Point3D) → Point3D` | Midpoint |
| `TranslatePoint3D` | `(Point3D, AnyRealNumber, AnyRealNumber, AnyRealNumber) → Point3D` | Translate |
| `ScalePoint3D` | `(Point3D, AnyRealNumber, Point3D) → Point3D` | Scale from center |
| `RotatePoint3DAroundX` | `(Point3D, AnyRealNumber) → Point3D` | Rotate around X axis |
| `RotatePoint3DAroundY` | `(Point3D, AnyRealNumber) → Point3D` | Rotate around Y axis |
| `RotatePoint3DAroundZ` | `(Point3D, AnyRealNumber) → Point3D` | Rotate around Z axis |
| `RotatePoint3DAroundAxis` | `(Point3D, Point3D, AnyRealNumber) → Point3D` | Rotate around arbitrary axis |
| `PointInSphere` | `(Point3D, Point3D, AnyRealNumber) → Boolean` | Point containment |
| `PointInBox` | `(Point3D, Point3D, Point3D) → Boolean` | Point containment |
| `AreaOfTriangle3D` | `(Point3D, Point3D, Point3D) → AnyRealNumber` | Triangle area |
| `SphereVolume` | `(AnyRealNumber) → AnyRealNumber` | (4/3)πr³ |
| `SphereSurfaceArea` | `(AnyRealNumber) → AnyRealNumber` | 4πr² |
| `CylinderVolume` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | πr²h |
| `CylinderSurfaceArea` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | 2πrh + 2πr² |
| `ConeVolume` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | (1/3)πr²h |
| `ConeSurfaceArea` | `(AnyRealNumber, AnyRealNumber) → AnyRealNumber` | πr√(r²+h²) + πr² |
| `BoxVolume` | `(AnyRealNumber, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | lwh |
| `BoxSurfaceArea` | `(AnyRealNumber, AnyRealNumber, AnyRealNumber) → AnyRealNumber` | 2(lw+lh+wh) |
| `PlaneFromPoints` | `(Point3D, Point3D, Point3D) → Tuple<AnyRealNumber, AnyRealNumber, AnyRealNumber, AnyRealNumber>` | Plane equation ax+by+cz+d=0 |
| `PointToPlaneDistance` | `(Point3D, Tuple<AnyRealNumber, AnyRealNumber, AnyRealNumber, AnyRealNumber>) → AnyRealNumber` | Point-plane distance |
| `LineToPlaneIntersection` | `(Point3D, Point3D, Tuple<AnyRealNumber, AnyRealNumber, AnyRealNumber, AnyRealNumber>) → Point3D \| Absent` | Line-plane intersection |

### 4.19 Number Classification

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsFinite` | `(AnyNumber) → Boolean` | Not infinite or NaN |
| `IsInfinite` | `(AnyNumber) → Boolean` | Positive or negative infinity |
| `IsNaN` | `(AnyNumber) → Boolean` | Not a number |
| `IsPositive` | `(AnyRealNumber) → Boolean` | Greater than zero |
| `IsNegative` | `(AnyRealNumber) → Boolean` | Less than zero |
| `IsZero` | `(AnyNumber) → Boolean` | Equal to zero |
| `IsPositiveZero` | `(AnyRealNumber) → Boolean` | Positive zero |
| `IsNegativeZero` | `(AnyRealNumber) → Boolean` | Negative zero |
| `IsInteger` | `(AnyNumber) → Boolean` | Has no fractional part |
| `IsEven` | `(Integer) → Boolean` | Divisible by 2 |
| `IsOdd` | `(Integer) → Boolean` | Not divisible by 2 |
| `IsPerfectSquare` | `(Integer) → Boolean` | Is n² for some integer n |
| `IsPerfectCube` | `(Integer) → Boolean` | Is n³ for some integer n |
| `IsPerfectPower` | `(Integer) → Boolean` | Is nᵏ for some integers n, k ≥ 2 |
| `IsReal` | `(AnyNumber) → Boolean` | Imaginary part is zero |
| `IsImaginary` | `(AnyNumber) → Boolean` | Real part is zero |
| `IsPurelyReal` | `(ComplexNumber) → Boolean` | Imaginary part is zero |
| `IsPurelyImaginary` | `(ComplexNumber) → Boolean` | Real part is zero |

### 4.20 Type Conversion (Numeric)

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ToInteger` | `(AnyNumber) → Integer` | Convert to integer (truncate) |
| `ToFraction` | `(AnyRealNumber) → Fraction` | Convert to fraction |
| `ToDecimalNumber` | `(AnyNumber) → DecimalNumber` | Convert to IEEE 754 float |
| `ToPrecisionNumber` | `(AnyRealNumber, Integer) → PrecisionNumber` | Convert with precision |
| `ToComplex` | `(AnyNumber) → ComplexNumber` | Convert to complex |

---

## 5. Text Operators

### 5.1 Basic Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Length` | `(Text) → Integer` | Number of characters |
| `ByteLength` | `(Text) → Integer` | Number of UTF-8 bytes |
| `CodePointCount` | `(Text) → Integer` | Number of Unicode code points |
| `GraphemeCount` | `(Text) → Integer` | Number of grapheme clusters |
| `IsEmpty` | `(Text) → Boolean` | Length is zero |
| `IsNotEmpty` | `(Text) → Boolean` | Length is not zero |
| `IsBlank` | `(Text) → Boolean` | Only whitespace |
| `IsNotBlank` | `(Text) → Boolean` | Has non-whitespace |

### 5.2 Concatenation and Joining

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Concat` | `(Text, Text, ...) → Text` | Concatenate text values |
| `Join` | `(List<Text>, Text) → Text` | Join with separator |
| `Repeat` | `(Text, Integer) → Text` | Repeat n times |
| `PadStart` | `(Text, Integer, Text) → Text` | Pad at start |
| `PadEnd` | `(Text, Integer, Text) → Text` | Pad at end |
| `PadBoth` | `(Text, Integer, Text) → Text` | Pad both sides |

### 5.3 Substring Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Substring` | `(Text, Integer, Integer) → Text` | Extract substring |
| `SubstringFrom` | `(Text, Integer) → Text` | Substring from index |
| `Left` | `(Text, Integer) → Text` | First n characters |
| `Right` | `(Text, Integer) → Text` | Last n characters |
| `CharacterAt` | `(Text, Integer) → Character` | Character at index |
| `CodePointAt` | `(Text, Integer) → Integer` | Code point at index |
| `First` | `(Text) → Character` | First character |
| `Last` | `(Text) → Character` | Last character |

### 5.4 Search and Position

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IndexOf` | `(Text, Text) → Integer \| Absent` | First occurrence index |
| `LastIndexOf` | `(Text, Text) → Integer \| Absent` | Last occurrence index |
| `IndexOfFrom` | `(Text, Text, Integer) → Integer \| Absent` | Index from position |
| `Contains` | `(Text, Text) → Boolean` | Contains substring |
| `StartsWith` | `(Text, Text) → Boolean` | Starts with prefix |
| `EndsWith` | `(Text, Text) → Boolean` | Ends with suffix |
| `CountOccurrences` | `(Text, Text) → Integer` | Count occurrences |
| `FindAll` | `(Text, Text) → List<Integer>` | All occurrence indices |

### 5.5 Replacement

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Replace` | `(Text, Text, Text) → Text` | Replace first occurrence |
| `ReplaceAll` | `(Text, Text, Text) → Text` | Replace all occurrences |
| `ReplaceAt` | `(Text, Integer, Integer, Text) → Text` | Replace at position |
| `Remove` | `(Text, Text) → Text` | Remove first occurrence |
| `RemoveAll` | `(Text, Text) → Text` | Remove all occurrences |
| `RemoveAt` | `(Text, Integer, Integer) → Text` | Remove at position |
| `Insert` | `(Text, Integer, Text) → Text` | Insert at position |

### 5.6 Splitting

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Split` | `(Text, Text) → List<Text>` | Split by delimiter |
| `SplitLimit` | `(Text, Text, Integer) → List<Text>` | Split with limit |
| `SplitLines` | `(Text) → List<Text>` | Split by line breaks |
| `SplitWords` | `(Text) → List<Text>` | Split by whitespace |
| `SplitCharacters` | `(Text) → List<Character>` | Split to characters |
| `SplitCodePoints` | `(Text) → List<Integer>` | Split to code points |
| `SplitGraphemes` | `(Text) → List<Text>` | Split to grapheme clusters |
| `Partition` | `(Text, Text) → Tuple<Text, Text, Text>` | Split around first occurrence |
| `PartitionLast` | `(Text, Text) → Tuple<Text, Text, Text>` | Split around last occurrence |

### 5.7 Case Conversion

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ToUpperCase` | `(Text) → Text` | Convert to uppercase |
| `ToLowerCase` | `(Text) → Text` | Convert to lowercase |
| `ToTitleCase` | `(Text) → Text` | Convert to title case |
| `Capitalize` | `(Text) → Text` | Capitalize first character |
| `SwapCase` | `(Text) → Text` | Swap case of each character |
| `ToCamelCase` | `(Text) → Text` | Convert to camelCase |
| `ToPascalCase` | `(Text) → Text` | Convert to PascalCase |
| `ToSnakeCase` | `(Text) → Text` | Convert to snake_case |
| `ToKebabCase` | `(Text) → Text` | Convert to kebab-case |
| `ToConstantCase` | `(Text) → Text` | Convert to CONSTANT_CASE |

### 5.8 Trimming

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Trim` | `(Text) → Text` | Trim whitespace both ends |
| `TrimStart` | `(Text) → Text` | Trim whitespace at start |
| `TrimEnd` | `(Text) → Text` | Trim whitespace at end |
| `TrimChars` | `(Text, Text) → Text` | Trim specified characters |
| `TrimCharsStart` | `(Text, Text) → Text` | Trim specified at start |
| `TrimCharsEnd` | `(Text, Text) → Text` | Trim specified at end |
| `CollapseWhitespace` | `(Text) → Text` | Collapse consecutive whitespace |
| `NormalizeWhitespace` | `(Text) → Text` | Normalize and trim whitespace |

### 5.9 Pattern Matching

| Operator | Signature | Description |
|----------|-----------|-------------|
| `MatchesPattern` | `(Text, Text) → Boolean` | Matches regex pattern |
| `FindPattern` | `(Text, Text) → Text \| Absent` | Find first match |
| `FindAllPatterns` | `(Text, Text) → List<Text>` | Find all matches |
| `ReplacePattern` | `(Text, Text, Text) → Text` | Replace first match |
| `ReplaceAllPatterns` | `(Text, Text, Text) → Text` | Replace all matches |
| `SplitByPattern` | `(Text, Text) → List<Text>` | Split by regex |
| `ExtractGroups` | `(Text, Text) → List<Text> \| Absent` | Extract capture groups |
| `ExtractAllGroups` | `(Text, Text) → List<List<Text>>` | Extract all groups |

### 5.10 Character Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `CharacterFromCodePoint` | `(Integer) → Character` | Character from code point |
| `CodePointFromCharacter` | `(Character) → Integer` | Code point from character |
| `CharacterName` | `(Character) → Text` | Unicode character name |
| `CharacterCategory` | `(Character) → Text` | Unicode general category |
| `IsUpperCase` | `(Character) → Boolean` | Is uppercase letter |
| `IsLowerCase` | `(Character) → Boolean` | Is lowercase letter |
| `IsLetter` | `(Character) → Boolean` | Is letter |
| `IsDigit` | `(Character) → Boolean` | Is decimal digit |
| `IsAlphanumeric` | `(Character) → Boolean` | Is letter or digit |
| `IsWhitespace` | `(Character) → Boolean` | Is whitespace |
| `IsPunctuation` | `(Character) → Boolean` | Is punctuation |
| `IsControl` | `(Character) → Boolean` | Is control character |
| `IsPrintable` | `(Character) → Boolean` | Is printable |
| `IsAscii` | `(Character) → Boolean` | Is ASCII (0-127) |

### 5.11 Unicode Normalization

| Operator | Signature | Description |
|----------|-----------|-------------|
| `NormalizeNFC` | `(Text) → Text` | Unicode NFC normalization |
| `NormalizeNFD` | `(Text) → Text` | Unicode NFD normalization |
| `NormalizeNFKC` | `(Text) → Text` | Unicode NFKC normalization |
| `NormalizeNFKD` | `(Text) → Text` | Unicode NFKD normalization |
| `Transliterate` | `(Text, Text) → Text` | Transliterate to script |
| `RemoveDiacritics` | `(Text) → Text` | Remove combining marks |

### 5.12 Encoding

| Operator | Signature | Description |
|----------|-----------|-------------|
| `EncodeUtf8` | `(Text) → List<Integer>` | Encode to UTF-8 bytes |
| `DecodeUtf8` | `(List<Integer>) → Text` | Decode from UTF-8 bytes |
| `EncodeBase64` | `(Text) → Text` | Encode to Base64 |
| `DecodeBase64` | `(Text) → Text` | Decode from Base64 |
| `EncodeHex` | `(Text) → Text` | Encode to hex text |
| `DecodeHex` | `(Text) → Text` | Decode from hex text |
| `EncodeUri` | `(Text) → Text` | URI encode |
| `DecodeUri` | `(Text) → Text` | URI decode |
| `EncodeUriComponent` | `(Text) → Text` | URI component encode |
| `DecodeUriComponent` | `(Text) → Text` | URI component decode |
| `EscapeHtml` | `(Text) → Text` | Escape HTML entities |
| `UnescapeHtml` | `(Text) → Text` | Unescape HTML entities |
| `EscapeXml` | `(Text) → Text` | Escape XML entities |
| `UnescapeXml` | `(Text) → Text` | Unescape XML entities |
| `EscapeJson` | `(Text) → Text` | Escape JSON text |
| `UnescapeJson` | `(Text) → Text` | Unescape JSON text |
| `EscapeRegex` | `(Text) → Text` | Escape regex special characters |

### 5.13 Validation

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsValidEmail` | `(Text) → Boolean` | Valid email format |
| `IsValidUrl` | `(Text) → Boolean` | Valid URL format |
| `IsValidIpv4` | `(Text) → Boolean` | Valid IPv4 address |
| `IsValidIpv6` | `(Text) → Boolean` | Valid IPv6 address |
| `IsValidUuid` | `(Text) → Boolean` | Valid UUID format |
| `IsValidHex` | `(Text) → Boolean` | Valid hex text |
| `IsValidBase64` | `(Text) → Boolean` | Valid Base64 text |
| `IsValidJson` | `(Text) → Boolean` | Valid JSON text |
| `IsValidNumeric` | `(Text) → Boolean` | Valid numeric text |
| `IsValidInteger` | `(Text) → Boolean` | Valid integer text |
| `IsValidIdentifier` | `(Text) → Boolean` | Valid identifier |
| `IsAllUpperCase` | `(Text) → Boolean` | All uppercase |
| `IsAllLowerCase` | `(Text) → Boolean` | All lowercase |
| `IsAllDigits` | `(Text) → Boolean` | All digits |
| `IsAllLetters` | `(Text) → Boolean` | All letters |
| `IsAllAlphanumeric` | `(Text) → Boolean` | All letters or digits |
| `IsAllAscii` | `(Text) → Boolean` | All ASCII characters |
| `IsAllPrintable` | `(Text) → Boolean` | All printable characters |

### 5.14 Comparison

| Operator | Signature | Description |
|----------|-----------|-------------|
| `CompareText` | `(Text, Text) → Integer` | Lexicographic comparison |
| `CompareTextIgnoreCase` | `(Text, Text) → Integer` | Case-insensitive comparison |
| `CompareNatural` | `(Text, Text) → Integer` | Natural sort comparison |
| `LevenshteinDistance` | `(Text, Text) → Integer` | Edit distance |
| `HammingDistance` | `(Text, Text) → Integer` | Hamming distance |
| `JaroWinklerSimilarity` | `(Text, Text) → DecimalNumber` | Jaro-Winkler similarity |
| `SorensenDiceCoefficient` | `(Text, Text) → DecimalNumber` | Dice coefficient |
| `LongestCommonSubsequence` | `(Text, Text) → Text` | LCS |
| `LongestCommonSubstring` | `(Text, Text) → Text` | Longest common substring |

### 5.15 Formatting

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Format` | `(Text, List<Any>) → Text` | Format with placeholders |
| `FormatNumber` | `(AnyNumber, Text) → Text` | Format number |
| `FormatCurrency` | `(AnyNumber, Text) → Text` | Format as currency |
| `FormatPercent` | `(AnyNumber, Integer) → Text` | Format as percentage |
| `FormatOrdinal` | `(Integer) → Text` | Format as ordinal |
| `Abbreviate` | `(Text, Integer) → Text` | Abbreviate with ellipsis |
| `WordWrap` | `(Text, Integer) → Text` | Wrap at word boundaries |
| `Truncate` | `(Text, Integer) → Text` | Truncate to length |
| `Center` | `(Text, Integer) → Text` | Center in width |
| `Slugify` | `(Text) → Text` | Convert to URL slug |

---

## 6. Temporal Operators

Temporal operators operate on **semantic temporal values** produced by schema validation (see §1.5). Codex surface parsing and canonicalization remain purely lexical; semantic temporal conversion and correctness checks are governed by the schema’s expected value types.

This section is a **Workshop/consuming-system operator set**, not Codex core. Codex defines surface recognition and schema value-type conformance; these operators define evaluation over the resulting semantic values.

Some operators additionally depend on runtime services (e.g., a clock for `Now`, a time zone database for `TimeZone`/`ZonedDateTime`). If a required runtime service is unavailable, evaluators must return `Invalid([...])`.

### 6.1 Construction

| Operator | Signature | Description |
|----------|-----------|-------------|
| `PlainDateFrom` | `(Integer, Integer, Integer) → PlainDate` | Create date (year, month, day) |
| `PlainTimeFrom` | `(Integer, Integer, Integer, Integer) → PlainTime` | Create time (h, m, s, ns) |
| `PlainDateTimeFrom` | `(Integer, Integer, Integer, Integer, Integer, Integer, Integer) → PlainDateTime` | Create datetime |
| `PlainYearMonthFrom` | `(Integer, Integer) → PlainYearMonth` | Create year-month |
| `PlainMonthDayFrom` | `(Integer, Integer) → PlainMonthDay` | Create month-day |
| `YearWeekFrom` | `(Integer, Integer) → YearWeek` | Create year-week |
| `InstantFromEpochMilliseconds` | `(Integer) → Instant` | From Unix timestamp |
| `InstantFromEpochSeconds` | `(Integer) → Instant` | From Unix seconds |
| `InstantFromEpochNanoseconds` | `(Integer) → Instant` | From Unix nanoseconds |
| `ZonedDateTimeFrom` | `(PlainDateTime, TimeZone) → ZonedDateTime` | Create zoned datetime |
| `DurationFrom` | `(Integer, Integer, Integer, Integer, Integer, Integer, Integer) → Duration` | Create duration |
| `DurationFromMilliseconds` | `(Integer) → Duration` | Duration from milliseconds |
| `DurationFromSeconds` | `(Integer) → Duration` | Duration from seconds |
| `DurationFromMinutes` | `(Integer) → Duration` | Duration from minutes |
| `DurationFromHours` | `(Integer) → Duration` | Duration from hours |
| `DurationFromDays` | `(Integer) → Duration` | Duration from days |
| `Now` | `() → Instant` | Current instant (fixed per document) |
| `Today` | `(TimeZone) → PlainDate` | Current date in timezone |
| `CurrentTime` | `(TimeZone) → PlainTime` | Current time in timezone |

### 6.2 Decomposition

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Year` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Year component |
| `Month` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Month (1-12) |
| `Day` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Day of month |
| `Hour` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Hour (0-23) |
| `Minute` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Minute (0-59) |
| `Second` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Second (0-59) |
| `Millisecond` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Millisecond |
| `Microsecond` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Microsecond |
| `Nanosecond` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Integer` | Nanosecond |
| `DayOfWeek` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Day of week (1=Mon) |
| `DayOfYear` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Day of year |
| `WeekOfYear` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | ISO week number |
| `Quarter` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Integer` | Quarter (1-4) |
| `EpochMilliseconds` | `(Instant) → Integer` | Unix timestamp ms |
| `EpochSeconds` | `(Instant) → Integer` | Unix timestamp s |
| `EpochNanoseconds` | `(Instant) → Integer` | Unix timestamp ns |
| `TimeZoneOf` | `(ZonedDateTime) → TimeZone` | Extract timezone |
| `OffsetSeconds` | `(ZonedDateTime) → Integer` | UTC offset in seconds |

### 6.3 Duration Decomposition

| Operator | Signature | Description |
|----------|-----------|-------------|
| `DurationYears` | `(Duration) → Integer` | Years component |
| `DurationMonths` | `(Duration) → Integer` | Months component |
| `DurationWeeks` | `(Duration) → Integer` | Weeks component |
| `DurationDays` | `(Duration) → Integer` | Days component |
| `DurationHours` | `(Duration) → Integer` | Hours component |
| `DurationMinutes` | `(Duration) → Integer` | Minutes component |
| `DurationSeconds` | `(Duration) → Integer` | Seconds component |
| `DurationMilliseconds` | `(Duration) → Integer` | Milliseconds component |
| `TotalMilliseconds` | `(Duration) → Integer` | Total milliseconds |
| `TotalSeconds` | `(Duration) → Integer` | Total seconds |
| `TotalMinutes` | `(Duration) → Integer` | Total minutes |
| `TotalHours` | `(Duration) → Integer` | Total hours |
| `TotalDays` | `(Duration) → Integer` | Total days |

### 6.4 Conversion

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ToPlainDate` | `(PlainDateTime \| ZonedDateTime) → PlainDate` | Extract date |
| `ToPlainTime` | `(PlainDateTime \| ZonedDateTime) → PlainTime` | Extract time |
| `ToPlainDateTime` | `(PlainDate, PlainTime) → PlainDateTime` | Combine date and time |
| `ToPlainYearMonth` | `(PlainDate \| PlainDateTime) → PlainYearMonth` | Extract year-month |
| `ToPlainMonthDay` | `(PlainDate \| PlainDateTime) → PlainMonthDay` | Extract month-day |
| `ToInstant` | `(ZonedDateTime) → Instant` | Convert to instant |
| `ToZonedDateTime` | `(Instant, TimeZone) → ZonedDateTime` | Convert to zoned |
| `InTimeZone` | `(ZonedDateTime, TimeZone) → ZonedDateTime` | Convert timezone |
| `ToLocalDateTime` | `(Instant, TimeZone) → PlainDateTime` | Convert to local time |

### 6.5 Arithmetic

| Operator | Signature | Description |
|----------|-----------|-------------|
| `AddDuration` | `(DeterministicTemporal, Duration) → DeterministicTemporal` | Add duration |
| `SubtractDuration` | `(DeterministicTemporal, Duration) → DeterministicTemporal` | Subtract duration |
| `AddYears` | `(PlainDate \| PlainDateTime \| ZonedDateTime, Integer) → Same` | Add years |
| `AddMonths` | `(PlainDate \| PlainDateTime \| ZonedDateTime, Integer) → Same` | Add months |
| `AddWeeks` | `(PlainDate \| PlainDateTime \| ZonedDateTime, Integer) → Same` | Add weeks |
| `AddDays` | `(PlainDate \| PlainDateTime \| ZonedDateTime, Integer) → Same` | Add days |
| `AddHours` | `(PlainTime \| PlainDateTime \| ZonedDateTime \| Instant, Integer) → Same` | Add hours |
| `AddMinutes` | `(PlainTime \| PlainDateTime \| ZonedDateTime \| Instant, Integer) → Same` | Add minutes |
| `AddSeconds` | `(PlainTime \| PlainDateTime \| ZonedDateTime \| Instant, Integer) → Same` | Add seconds |
| `AddMilliseconds` | `(PlainTime \| PlainDateTime \| ZonedDateTime \| Instant, Integer) → Same` | Add milliseconds |
| `DurationBetween` | `(DeterministicTemporal, DeterministicTemporal) → Duration` | Duration between |
| `DifferenceInYears` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Years between |
| `DifferenceInMonths` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Months between |
| `DifferenceInWeeks` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Weeks between |
| `DifferenceInDays` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Days between |
| `DifferenceInHours` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Hours between |
| `DifferenceInMinutes` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Minutes between |
| `DifferenceInSeconds` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Seconds between |
| `DifferenceInMilliseconds` | `(DeterministicTemporal, DeterministicTemporal) → Integer` | Milliseconds between |
| `NegateDuration` | `(Duration) → Duration` | Negate duration |
| `AbsoluteDuration` | `(Duration) → Duration` | Absolute value |
| `MultiplyDuration` | `(Duration, Integer) → Duration` | Multiply duration |
| `DivideDuration` | `(Duration, Integer) → Duration` | Divide duration |

### 6.6 Comparison

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsBefore` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | First is before second |
| `IsAfter` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | First is after second |
| `IsSameOrBefore` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | First is same or before |
| `IsSameOrAfter` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | First is same or after |
| `IsSameInstant` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | Same point in time |
| `IsSameDay` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | Same calendar day |
| `IsSameMonth` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | Same month |
| `IsSameYear` | `(DeterministicTemporal, DeterministicTemporal) → Boolean` | Same year |
| `IsInRange` | `(DeterministicTemporal, DeterministicTemporal, DeterministicTemporal) → Boolean` | In range (inclusive), per the semantic temporal model |
| `EarliestOf` | `(DeterministicTemporal, DeterministicTemporal, ...) → DeterministicTemporal` | Earliest value, per the semantic temporal model |
| `LatestOf` | `(DeterministicTemporal, DeterministicTemporal, ...) → DeterministicTemporal` | Latest value, per the semantic temporal model |

### 6.7 Rounding

| Operator | Signature | Description |
|----------|-----------|-------------|
| `RoundToYear` | `(PlainDate \| PlainDateTime) → Same` | Round to year |
| `RoundToMonth` | `(PlainDate \| PlainDateTime) → Same` | Round to month |
| `RoundToWeek` | `(PlainDate \| PlainDateTime) → Same` | Round to week |
| `RoundToDay` | `(PlainDateTime \| ZonedDateTime) → Same` | Round to day |
| `RoundToHour` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Same` | Round to hour |
| `RoundToMinute` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Same` | Round to minute |
| `RoundToSecond` | `(PlainTime \| PlainDateTime \| ZonedDateTime) → Same` | Round to second |
| `StartOfYear` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | First day of year |
| `EndOfYear` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | Last day of year |
| `StartOfMonth` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | First day of month |
| `EndOfMonth` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | Last day of month |
| `StartOfWeek` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | First day of week |
| `EndOfWeek` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Same` | Last day of week |
| `StartOfDay` | `(PlainDateTime \| ZonedDateTime) → Same` | Start of day |
| `EndOfDay` | `(PlainDateTime \| ZonedDateTime) → Same` | End of day |

### 6.8 Calendar Information

| Operator | Signature | Description |
|----------|-----------|-------------|
| `DaysInMonth` | `(PlainDate \| PlainYearMonth) → Integer` | Days in month |
| `DaysInYear` | `(PlainDate \| Integer) → Integer` | Days in year |
| `IsLeapYear` | `(PlainDate \| Integer) → Boolean` | Is leap year |
| `IsWeekend` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Boolean` | Is Saturday/Sunday |
| `IsWeekday` | `(PlainDate \| PlainDateTime \| ZonedDateTime) → Boolean` | Is Monday-Friday |
| `WeeksInYear` | `(Integer) → Integer` | ISO weeks in year |

### 6.9 Formatting

| Operator | Signature | Description |
|----------|-----------|-------------|
| `FormatTemporal` | `(Temporal, Text) → Text` | Format with pattern (keywords pass through unless renderer resolves them) |
| `FormatIso8601` | `(Temporal) → Text` | ISO 8601 format (keywords pass through unless renderer resolves them) |
| `FormatRfc2822` | `(ZonedDateTime \| Instant) → Text` | RFC 2822 format |
| `FormatRfc3339` | `(ZonedDateTime \| Instant) → Text` | RFC 3339 format |
| `ParsePlainDate` | `(Text, Text) → PlainDate` | Parse date from text |
| `ParsePlainTime` | `(Text, Text) → PlainTime` | Parse time from text |
| `ParsePlainDateTime` | `(Text, Text) → PlainDateTime` | Parse datetime from text |
| `ParseInstant` | `(Text) → Instant` | Parse ISO instant |

### 6.10 Temporal Type Guards

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsPlainDate` | `(Any) → Boolean` | Is PlainDate |
| `IsPlainTime` | `(Any) → Boolean` | Is PlainTime |
| `IsPlainDateTime` | `(Any) → Boolean` | Is PlainDateTime |
| `IsPlainYearMonth` | `(Any) → Boolean` | Is PlainYearMonth |
| `IsPlainMonthDay` | `(Any) → Boolean` | Is PlainMonthDay |
| `IsYearWeek` | `(Any) → Boolean` | Is YearWeek |
| `IsInstant` | `(Any) → Boolean` | Is Instant |
| `IsZonedDateTime` | `(Any) → Boolean` | Is ZonedDateTime |
| `IsDuration` | `(Any) → Boolean` | Is Duration |
| `IsTimeZone` | `(Any) → Boolean` | Is TimeZone |
| `IsCalendar` | `(Any) → Boolean` | Is Calendar |
| `IsTemporal` | `(Any) → Boolean` | Is any temporal type |

---

## 7. Collection Operators

### 7.1 List Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Count` | `(List<T>) → Integer` | Number of elements |
| `IsEmpty` | `(List<T>) → Boolean` | Has no elements |
| `IsNotEmpty` | `(List<T>) → Boolean` | Has elements |
| `FirstElement` | `(List<T>) → T \| Absent` | First element |
| `LastElement` | `(List<T>) → T \| Absent` | Last element |
| `ElementAt` | `(List<T>, Integer) → T \| Absent` | Element at index |
| `IndexOf` | `(List<T>, T) → Integer \| Absent` | Index of element |
| `LastIndexOf` | `(List<T>, T) → Integer \| Absent` | Last index of element |
| `Contains` | `(List<T>, T) → Boolean` | Contains element |
| `ContainsAll` | `(List<T>, List<T>) → Boolean` | Contains all elements |
| `ContainsAny` | `(List<T>, List<T>) → Boolean` | Contains any element |

### 7.2 List Transformation

| Operator | Signature | Description |
|----------|-----------|-------------|
| `MapElements` | `(List<T>, T → U) → List<U>` | Transform each element |
| `FilterElements` | `(List<T>, T → Boolean) → List<T>` | Filter by predicate |
| `ReduceElements` | `(List<T>, (U, T) → U, U) → U` | Reduce to single value |
| `FlatMapElements` | `(List<T>, T → List<U>) → List<U>` | Map and flatten |
| `Reverse` | `(List<T>) → List<T>` | Reverse order |
| `SortBy` | `(List<T>, T → OrderableRealNumber) → List<T>` | Sort by key |
| `SortByDescending` | `(List<T>, T → OrderableRealNumber) → List<T>` | Sort descending |
| `SortWith` | `(List<T>, (T, T) → Integer) → List<T>` | Sort with comparator |
| `Distinct` | `(List<T>) → List<T>` | Remove duplicates |
| `DistinctBy` | `(List<T>, T → U) → List<T>` | Remove duplicates by key |
| `Flatten` | `(List<List<T>>) → List<T>` | Flatten nested lists |
| `FlattenDepth` | `(List<Any>, Integer) → List<Any>` | Flatten to depth |
| `Interleave` | `(List<T>, List<T>) → List<T>` | Interleave elements |
| `Intersperse` | `(List<T>, T) → List<T>` | Insert between elements |

### 7.3 List Slicing

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Slice` | `(List<T>, Integer, Integer) → List<T>` | Extract slice |
| `Take` | `(List<T>, Integer) → List<T>` | Take first n |
| `TakeLast` | `(List<T>, Integer) → List<T>` | Take last n |
| `TakeWhile` | `(List<T>, T → Boolean) → List<T>` | Take while predicate |
| `Drop` | `(List<T>, Integer) → List<T>` | Drop first n |
| `DropLast` | `(List<T>, Integer) → List<T>` | Drop last n |
| `DropWhile` | `(List<T>, T → Boolean) → List<T>` | Drop while predicate |
| `Chunk` | `(List<T>, Integer) → List<List<T>>` | Split into chunks |
| `SlidingWindow` | `(List<T>, Integer) → List<List<T>>` | Sliding windows |
| `SlidingWindowStep` | `(List<T>, Integer, Integer) → List<List<T>>` | Sliding with step |

### 7.4 List Modification

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Append` | `(List<T>, T) → List<T>` | Add to end |
| `Prepend` | `(List<T>, T) → List<T>` | Add to start |
| `InsertAt` | `(List<T>, Integer, T) → List<T>` | Insert at index |
| `RemoveAt` | `(List<T>, Integer) → List<T>` | Remove at index |
| `RemoveElement` | `(List<T>, T) → List<T>` | Remove first occurrence |
| `RemoveAllElements` | `(List<T>, T) → List<T>` | Remove all occurrences |
| `ReplaceAt` | `(List<T>, Integer, T) → List<T>` | Replace at index |
| `ReplaceElement` | `(List<T>, T, T) → List<T>` | Replace first occurrence |
| `ReplaceAllElements` | `(List<T>, T, T) → List<T>` | Replace all occurrences |
| `UpdateAt` | `(List<T>, Integer, T → T) → List<T>` | Update at index |
| `Concatenate` | `(List<T>, List<T>) → List<T>` | Concatenate lists |

### 7.5 List Combining

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Zip` | `(List<T>, List<U>) → List<Tuple<T, U>>` | Zip two lists |
| `ZipWith` | `(List<T>, List<U>, (T, U) → V) → List<V>` | Zip with function |
| `Unzip` | `(List<Tuple<T, U>>) → Tuple<List<T>, List<U>>` | Unzip to two lists |
| `CartesianProduct` | `(List<T>, List<U>) → List<Tuple<T, U>>` | Cartesian product |

### 7.6 List Partitioning

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Partition` | `(List<T>, T → Boolean) → Tuple<List<T>, List<T>>` | Partition by predicate |
| `GroupBy` | `(List<T>, T → K) → Map<K, List<T>>` | Group by key |
| `GroupByAggregate` | `(List<T>, T → K, List<T> → V) → Map<K, V>` | Group and aggregate |
| `SplitAt` | `(List<T>, Integer) → Tuple<List<T>, List<T>>` | Split at index |
| `SplitWhen` | `(List<T>, T → Boolean) → List<List<T>>` | Split when predicate |

### 7.7 List Predicates

| Operator | Signature | Description |
|----------|-----------|-------------|
| `All` | `(List<T>, T → Boolean) → Boolean` | All match predicate |
| `Any` | `(List<T>, T → Boolean) → Boolean` | Any matches predicate |
| `None` | `(List<T>, T → Boolean) → Boolean` | None match predicate |
| `CountWhere` | `(List<T>, T → Boolean) → Integer` | Count matching |

### 7.8 List Aggregation

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Sum` | `(List<AnyNumber>) → AnyNumber` | Sum of elements |
| `Product` | `(List<AnyNumber>) → AnyNumber` | Product of elements |
| `Minimum` | `(List<OrderableRealNumber>) → OrderableRealNumber \| Absent` | Minimum element |
| `Maximum` | `(List<OrderableRealNumber>) → OrderableRealNumber \| Absent` | Maximum element |
| `MinimumBy` | `(List<T>, T → OrderableRealNumber) → T \| Absent` | Element with min key |
| `MaximumBy` | `(List<T>, T → OrderableRealNumber) → T \| Absent` | Element with max key |
| `Average` | `(List<AnyNumber>) → AnyRealNumber` | Arithmetic mean |

### 7.9 Set Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `SetCount` | `(Set<T>) → Integer` | Number of elements |
| `SetIsEmpty` | `(Set<T>) → Boolean` | Has no elements |
| `SetContains` | `(Set<T>, T) → Boolean` | Contains element |
| `SetAdd` | `(Set<T>, T) → Set<T>` | Add element |
| `SetRemove` | `(Set<T>, T) → Set<T>` | Remove element |
| `SetUnion` | `(Set<T>, Set<T>) → Set<T>` | Union |
| `SetIntersection` | `(Set<T>, Set<T>) → Set<T>` | Intersection |
| `SetDifference` | `(Set<T>, Set<T>) → Set<T>` | Difference |
| `SetSymmetricDifference` | `(Set<T>, Set<T>) → Set<T>` | Symmetric difference |
| `IsSubsetOf` | `(Set<T>, Set<T>) → Boolean` | Is subset |
| `IsSupersetOf` | `(Set<T>, Set<T>) → Boolean` | Is superset |
| `IsProperSubsetOf` | `(Set<T>, Set<T>) → Boolean` | Is proper subset |
| `IsProperSupersetOf` | `(Set<T>, Set<T>) → Boolean` | Is proper superset |
| `IsDisjointFrom` | `(Set<T>, Set<T>) → Boolean` | No common elements |
| `ToList` | `(Set<T>) → List<T>` | Convert to list |
| `ToSet` | `(List<T>) → Set<T>` | Convert to set |

### 7.10 Map Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `MapCount` | `(Map<K, V>) → Integer` | Number of entries |
| `MapIsEmpty` | `(Map<K, V>) → Boolean` | Has no entries |
| `MapGet` | `(Map<K, V>, K) → V \| Absent` | Get value by key |
| `MapGetOrDefault` | `(Map<K, V>, K, V) → V` | Get with default |
| `MapContainsKey` | `(Map<K, V>, K) → Boolean` | Contains key |
| `MapContainsValue` | `(Map<K, V>, V) → Boolean` | Contains value |
| `MapPut` | `(Map<K, V>, K, V) → Map<K, V>` | Add/update entry |
| `MapPutAll` | `(Map<K, V>, Map<K, V>) → Map<K, V>` | Add all entries |
| `MapRemove` | `(Map<K, V>, K) → Map<K, V>` | Remove by key |
| `MapRemoveAll` | `(Map<K, V>, List<K>) → Map<K, V>` | Remove multiple keys |
| `MapKeys` | `(Map<K, V>) → Set<K>` | All keys |
| `MapValues` | `(Map<K, V>) → List<V>` | All values |
| `MapEntries` | `(Map<K, V>) → List<Tuple<K, V>>` | All entries |
| `MapMapValues` | `(Map<K, V>, V → W) → Map<K, W>` | Transform values |
| `MapMapKeys` | `(Map<K, V>, K → L) → Map<L, V>` | Transform keys |
| `MapFilterEntries` | `(Map<K, V>, (K, V) → Boolean) → Map<K, V>` | Filter entries |
| `MapMerge` | `(Map<K, V>, Map<K, V>, (V, V) → V) → Map<K, V>` | Merge with resolver |
| `MapFromEntries` | `(List<Tuple<K, V>>) → Map<K, V>` | Create from entries |
| `MapFromLists` | `(List<K>, List<V>) → Map<K, V>` | Create from parallel lists |
| `MapInvert` | `(Map<K, V>) → Map<V, K>` | Swap keys and values |

### 7.11 Record Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `RecordGet` | `(Record, Text) → Any \| Absent` | Get field value |
| `RecordGetOrDefault` | `(Record, Text, Any) → Any` | Get with default |
| `RecordHasField` | `(Record, Text) → Boolean` | Has field |
| `RecordPut` | `(Record, Text, Any) → Record` | Add/update field |
| `RecordRemove` | `(Record, Text) → Record` | Remove field |
| `RecordKeys` | `(Record) → Set<Text>` | All field names |
| `RecordValues` | `(Record) → List<Any>` | All field values |
| `RecordMerge` | `(Record, Record) → Record` | Merge records |
| `RecordPick` | `(Record, List<Text>) → Record` | Pick fields |
| `RecordOmit` | `(Record, List<Text>) → Record` | Omit fields |
| `RecordMapValues` | `(Record, Any → Any) → Record` | Transform values |
| `RecordFilterFields` | `(Record, (Text, Any) → Boolean) → Record` | Filter fields |
| `RecordRenameField` | `(Record, Text, Text) → Record` | Rename field |

### 7.12 Tuple Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `TupleFirst` | `(Tuple<T, ...>) → T` | First element |
| `TupleSecond` | `(Tuple<T1, T2, ...>) → T2` | Second element |
| `TupleThird` | `(Tuple<T1, T2, T3, ...>) → T3` | Third element |
| `TupleNth` | `(Tuple<...>, Integer) → Any` | nth element |
| `TupleCount` | `(Tuple<...>) → Integer` | Number of elements |
| `TupleToList` | `(Tuple<T, T, ...>) → List<T>` | Convert to list |
| `TupleConcat` | `(Tuple<...>, Tuple<...>) → Tuple<...>` | Concatenate tuples |

### 7.13 Range Operations

Range Values are declarative intervals. Per Codex §5.17, Codex-conforming tools must not enumerate Range Values; evaluators therefore must not expand a range into its member values.

In practice, the most common ranges are numeric, temporal, and character ranges. Text ranges can also be useful when a schema defines a lexical ordering. Other range semantics are permitted but must be defined by the governing schema or consuming system.

Ranges are declarative endpoints; they do not imply enumeration of intermediate values.

| Operator | Signature | Description |
|----------|-----------|-------------|
| `RangeFrom` | `(T, T) → Range<T>` | Create range |
| `RangeFromWithStep` | `(T, T, T) → Range<T>` | Range with step |
| `RangeStart` | `(Range<T>) → T` | Start value |
| `RangeEnd` | `(Range<T>) → T` | End value |
| `RangeStep` | `(Range<T>) → T \| Absent` | Step value |
| `RangeContains` | `(Range<T>, T) → Boolean` | Contains value |
| `RangeToList` | `(Range<Integer>) → List<Integer>` | Enumerate to list (non-conforming; must return Invalid) |
| `RangeLength` | `(Range<Integer>) → Integer` | Number of values (non-conforming; must return Invalid) |
| `RangeIsEmpty` | `(Range<T>) → Boolean` | Is empty range |
| `RangeOverlaps` | `(Range<T>, Range<T>) → Boolean` | Ranges overlap |
| `RangeIntersection` | `(Range<T>, Range<T>) → Range<T> \| Absent` | Intersection |
| `RangeUnion` | `(Range<T>, Range<T>) → Range<T> \| Absent` | Union (if contiguous) |

### 7.14 Join Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `InnerJoin` | `(List<T>, List<U>, T → K, U → K) → List<Tuple<T, U>>` | Inner join |
| `LeftJoin` | `(List<T>, List<U>, T → K, U → K) → List<Tuple<T, U \| Absent>>` | Left join |
| `RightJoin` | `(List<T>, List<U>, T → K, U → K) → List<Tuple<T \| Absent, U>>` | Right join |
| `FullJoin` | `(List<T>, List<U>, T → K, U → K) → List<Tuple<T \| Absent, U \| Absent>>` | Full outer join |
| `CrossJoin` | `(List<T>, List<U>) → List<Tuple<T, U>>` | Cross join |

---

## 8. Color Operators

### 8.1 Construction

| Operator | Signature | Description |
|----------|-----------|-------------|
| `RgbColorFrom` | `(Integer, Integer, Integer) → RgbColor` | From R, G, B (0-255) |
| `RgbaColorFrom` | `(Integer, Integer, Integer, DecimalNumber) → RgbColor` | With alpha |
| `HslColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → HslColor` | From H, S, L |
| `HslaColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber, DecimalNumber) → HslColor` | With alpha |
| `HsvColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → HsvColor` | From H, S, V |
| `HwbColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → HwbColor` | From H, W, B |
| `LabColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → LabColor` | From L, a, b |
| `LchColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → LchColor` | From L, C, H |
| `OklabColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → OklabColor` | From L, a, b |
| `OklchColorFrom` | `(DecimalNumber, DecimalNumber, DecimalNumber) → OklchColor` | From L, C, H |
| `HexColorFrom` | `(Text) → HexColor` | From hex text |
| `NamedColor` | `(Text) → RgbColor` | From CSS color name |

### 8.2 Decomposition

| Operator | Signature | Description |
|----------|-----------|-------------|
| `RedChannel` | `(Color) → Integer` | Red component (0-255) |
| `GreenChannel` | `(Color) → Integer` | Green component (0-255) |
| `BlueChannel` | `(Color) → Integer` | Blue component (0-255) |
| `AlphaChannel` | `(Color) → DecimalNumber` | Alpha (0-1) |
| `Hue` | `(Color) → DecimalNumber` | Hue (0-360) |
| `Saturation` | `(Color) → DecimalNumber` | Saturation (0-1) |
| `Lightness` | `(Color) → DecimalNumber` | Lightness (0-1) |
| `Value` | `(Color) → DecimalNumber` | Value/brightness (0-1) |
| `LabL` | `(LabColor \| LchColor) → DecimalNumber` | L component |
| `LabA` | `(LabColor) → DecimalNumber` | a component |
| `LabB` | `(LabColor) → DecimalNumber` | b component |
| `LchC` | `(LchColor) → DecimalNumber` | Chroma |
| `LchH` | `(LchColor) → DecimalNumber` | Hue angle |
| `OklabL` | `(OklabColor \| OklchColor) → DecimalNumber` | Oklab L |
| `OklabA` | `(OklabColor) → DecimalNumber` | Oklab a |
| `OklabB` | `(OklabColor) → DecimalNumber` | Oklab b |
| `OklchC` | `(OklchColor) → DecimalNumber` | Oklch chroma |
| `OklchH` | `(OklchColor) → DecimalNumber` | Oklch hue |

### 8.3 Conversion

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ToRgb` | `(Color) → RgbColor` | Convert to RGB |
| `ToHsl` | `(Color) → HslColor` | Convert to HSL |
| `ToHsv` | `(Color) → HsvColor` | Convert to HSV |
| `ToHwb` | `(Color) → HwbColor` | Convert to HWB |
| `ToLab` | `(Color) → LabColor` | Convert to Lab |
| `ToLch` | `(Color) → LchColor` | Convert to LCH |
| `ToOklab` | `(Color) → OklabColor` | Convert to Oklab |
| `ToOklch` | `(Color) → OklchColor` | Convert to Oklch |
| `ToHex` | `(Color) → HexColor` | Convert to hex |
| `ToCssString` | `(Color) → Text` | CSS color string |

### 8.4 Manipulation

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Lighten` | `(Color, DecimalNumber) → Color` | Increase lightness |
| `Darken` | `(Color, DecimalNumber) → Color` | Decrease lightness |
| `Saturate` | `(Color, DecimalNumber) → Color` | Increase saturation |
| `Desaturate` | `(Color, DecimalNumber) → Color` | Decrease saturation |
| `RotateHue` | `(Color, DecimalNumber) → Color` | Rotate hue angle |
| `AdjustHue` | `(Color, DecimalNumber) → Color` | Adjust hue |
| `SetAlpha` | `(Color, DecimalNumber) → Color` | Set alpha |
| `FadeIn` | `(Color, DecimalNumber) → Color` | Increase alpha |
| `FadeOut` | `(Color, DecimalNumber) → Color` | Decrease alpha |
| `Grayscale` | `(Color) → Color` | Convert to grayscale |
| `Complement` | `(Color) → Color` | Complementary color |
| `Invert` | `(Color) → Color` | Invert color |
| `SetLightness` | `(Color, DecimalNumber) → Color` | Set lightness |
| `SetSaturation` | `(Color, DecimalNumber) → Color` | Set saturation |
| `SetHue` | `(Color, DecimalNumber) → Color` | Set hue |
| `AdjustRed` | `(Color, Integer) → Color` | Adjust red |
| `AdjustGreen` | `(Color, Integer) → Color` | Adjust green |
| `AdjustBlue` | `(Color, Integer) → Color` | Adjust blue |

### 8.5 Mixing

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Mix` | `(Color, Color, DecimalNumber) → Color` | Mix two colors |
| `MixInColorSpace` | `(Color, Color, DecimalNumber, Text) → Color` | Mix in color space |
| `Blend` | `(Color, Color, Text) → Color` | Blend with mode |
| `Average` | `(List<Color>) → Color` | Average of colors |
| `AverageInColorSpace` | `(List<Color>, Text) → Color` | Average in space |

### 8.6 Analysis

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Luminance` | `(Color) → DecimalNumber` | Relative luminance |
| `ContrastRatio` | `(Color, Color) → DecimalNumber` | WCAG contrast ratio |
| `ColorDifference` | `(Color, Color) → DecimalNumber` | Euclidean distance |
| `DeltaE` | `(Color, Color) → DecimalNumber` | CIE Delta E |
| `DeltaE2000` | `(Color, Color) → DecimalNumber` | CIEDE2000 |
| `IsLight` | `(Color) → Boolean` | Luminance > 0.5 |
| `IsDark` | `(Color) → Boolean` | Luminance <= 0.5 |
| `MeetsContrastRatio` | `(Color, Color, DecimalNumber) → Boolean` | Meets ratio |
| `MeetsWcagAA` | `(Color, Color) → Boolean` | Meets WCAG AA |
| `MeetsWcagAAA` | `(Color, Color) → Boolean` | Meets WCAG AAA |
| `MeetsWcagAALargeText` | `(Color, Color) → Boolean` | AA large text |
| `MeetsWcagAAALargeText` | `(Color, Color) → Boolean` | AAA large text |

### 8.7 Harmonies

| Operator | Signature | Description |
|----------|-----------|-------------|
| `ComplementaryPair` | `(Color) → Tuple<Color, Color>` | Complementary pair |
| `TriadicColors` | `(Color) → Tuple<Color, Color, Color>` | Triadic harmony |
| `TetradicColors` | `(Color) → Tuple<Color, Color, Color, Color>` | Tetradic harmony |
| `AnalogousColors` | `(Color) → Tuple<Color, Color, Color>` | Analogous harmony |
| `SplitComplementary` | `(Color) → Tuple<Color, Color, Color>` | Split complementary |
| `SquareColors` | `(Color) → Tuple<Color, Color, Color, Color>` | Square harmony |

### 8.8 Palettes

| Operator | Signature | Description |
|----------|-----------|-------------|
| `Tints` | `(Color, Integer) → List<Color>` | Tint scale |
| `Shades` | `(Color, Integer) → List<Color>` | Shade scale |
| `Tones` | `(Color, Integer) → List<Color>` | Tone scale |
| `Monochromatic` | `(Color, Integer) → List<Color>` | Monochromatic palette |
| `GradientStops` | `(Color, Color, Integer) → List<Color>` | Gradient colors |
| `GradientStopsInColorSpace` | `(Color, Color, Integer, Text) → List<Color>` | Gradient in space |

### 8.9 Color Type Guards

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsColor` | `(Any) → Boolean` | Is any color type |
| `IsRgbColor` | `(Any) → Boolean` | Is RGB color |
| `IsHslColor` | `(Any) → Boolean` | Is HSL color |
| `IsHsvColor` | `(Any) → Boolean` | Is HSV color |
| `IsLabColor` | `(Any) → Boolean` | Is Lab color |
| `IsLchColor` | `(Any) → Boolean` | Is LCH color |
| `IsOklabColor` | `(Any) → Boolean` | Is Oklab color |
| `IsOklchColor` | `(Any) → Boolean` | Is Oklch color |
| `IsHexColor` | `(Any) → Boolean` | Is hex color |

---

## 9. Identity Operators

### 9.1 UUID Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `UuidFromString` | `(Text) → Uuid` | Parse UUID string |
| `UuidToString` | `(Uuid) → Text` | UUID to string |
| `UuidVersion` | `(Uuid) → Integer` | UUID version |
| `UuidVariant` | `(Uuid) → Integer` | UUID variant |
| `UuidTimestamp` | `(Uuid) → Instant \| Absent` | Timestamp (v1/v6/v7) |
| `UuidCompare` | `(Uuid, Uuid) → Integer` | Compare UUIDs |
| `IsNilUuid` | `(Uuid) → Boolean` | Is nil UUID |
| `IsMaxUuid` | `(Uuid) → Boolean` | Is max UUID |

### 9.2 IRI Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IriFromString` | `(Text) → IriReference` | Parse IRI string |
| `IriToString` | `(IriReference) → Text` | IRI to string |
| `IriScheme` | `(IriReference) → Text \| Absent` | Extract scheme |
| `IriAuthority` | `(IriReference) → Text \| Absent` | Extract authority |
| `IriHost` | `(IriReference) → Text \| Absent` | Extract host |
| `IriPort` | `(IriReference) → Integer \| Absent` | Extract port |
| `IriPath` | `(IriReference) → Text` | Extract path |
| `IriQuery` | `(IriReference) → Text \| Absent` | Extract query |
| `IriFragment` | `(IriReference) → Text \| Absent` | Extract fragment |
| `IriResolve` | `(IriReference, IriReference) → IriReference` | Resolve relative IRI |
| `IriRelativize` | `(IriReference, IriReference) → IriReference` | Make relative |
| `IriNormalize` | `(IriReference) → IriReference` | Normalize IRI |
| `IsAbsoluteIri` | `(IriReference) → Boolean` | Is absolute |
| `IsRelativeIri` | `(IriReference) → Boolean` | Is relative |

### 9.3 Lookup Token Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `LookupTokenFromString` | `(Text) → LookupToken` | Parse lookup token |
| `LookupTokenToString` | `(LookupToken) → Text` | Token to string |
| `LookupTokenName` | `(LookupToken) → Text` | Extract name |
| `LookupTokenCompare` | `(LookupToken, LookupToken) → Integer` | Compare tokens |

### 9.4 Enumerated Token Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `EnumeratedTokenFromString` | `(Text) → EnumeratedToken` | Parse enumerated token |
| `EnumeratedTokenToString` | `(EnumeratedToken) → Text` | Token to string |
| `EnumeratedTokenName` | `(EnumeratedToken) → Text` | Extract name |
| `EnumeratedTokenCompare` | `(EnumeratedToken, EnumeratedToken) → Integer` | Compare tokens |

### 9.5 Identity Type Guards

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsUuid` | `(Any) → Boolean` | Is UUID |
| `IsIriReference` | `(Any) → Boolean` | Is IRI |
| `IsLookupToken` | `(Any) → Boolean` | Is lookup token |
| `IsEnumeratedToken` | `(Any) → Boolean` | Is enumerated token |
| `IsHostName` | `(Any) → Boolean` | Is host name |
| `IsEmailAddress` | `(Any) → Boolean` | Is email address |
| `IsUrl` | `(Any) → Boolean` | Is URL |

### 9.6 Host / Email / URL Operations

| Operator | Signature | Description |
|----------|-----------|-------------|
| `HostNameFromString` | `(Text) → HostName` | Parse and canonicalize hostname |
| `HostNameToString` | `(HostName) → Text` | Canonical hostname text |
| `EmailAddressFromString` | `(Text) → EmailAddress` | Parse and canonicalize email address |
| `EmailAddressToString` | `(EmailAddress) → Text` | Canonical email address text |
| `UrlFromString` | `(Text) → Url` | Parse and canonicalize URL |
| `UrlFromStringWithBase` | `(Text, Text) → Url` | Resolve relative URL against base and canonicalize |
| `UrlToString` | `(Url) → Text` | Canonical URL text |

---

## 10. Relational and Logic Operators

### 10.1 Equality

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsEqualTo` | `(T, T) → Boolean` | Structural equality |
| `IsNotEqualTo` | `(T, T) → Boolean` | Structural inequality |
| `IsIdenticalTo` | `(T, T) → Boolean` | Reference identity |
| `IsNotIdenticalTo` | `(T, T) → Boolean` | Reference non-identity |

### 10.2 Ordering

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsLessThan` | `(OrderableRealNumber, OrderableRealNumber) → Boolean` | Less than |
| `IsLessThanOrEqualTo` | `(OrderableRealNumber, OrderableRealNumber) → Boolean` | Less than or equal |
| `IsGreaterThan` | `(OrderableRealNumber, OrderableRealNumber) → Boolean` | Greater than |
| `IsGreaterThanOrEqualTo` | `(OrderableRealNumber, OrderableRealNumber) → Boolean` | Greater or equal |
| `Compare` | `(OrderableRealNumber, OrderableRealNumber) → Integer` | -1, 0, or 1 |
| `IsBetween` | `(OrderableRealNumber, OrderableRealNumber, OrderableRealNumber) → Boolean` | In range (inclusive) |
| `IsBetweenExclusive` | `(OrderableRealNumber, OrderableRealNumber, OrderableRealNumber) → Boolean` | In range (exclusive) |

### 10.3 Boolean Composition

| Operator | Signature | Description |
|----------|-----------|-------------|
| `And` | `(Boolean, Boolean, ...) → Boolean` | Logical AND |
| `Or` | `(Boolean, Boolean, ...) → Boolean` | Logical OR |
| `Not` | `(Boolean) → Boolean` | Logical NOT |
| `Xor` | `(Boolean, Boolean) → Boolean` | Exclusive OR |
| `Nand` | `(Boolean, Boolean) → Boolean` | NOT AND |
| `Nor` | `(Boolean, Boolean) → Boolean` | NOT OR |
| `Implies` | `(Boolean, Boolean) → Boolean` | Logical implication |
| `Iff` | `(Boolean, Boolean) → Boolean` | If and only if |

### 10.4 Control Flow

| Operator | Signature | Description |
|----------|-----------|-------------|
| `If` | `(Boolean, T, T) → T` | Conditional |
| `IfAbsent` | `(T \| Absent, T) → T` | Default if absent |
| `Coalesce` | `(T \| Absent, T \| Absent, ...) → T \| Absent` | First non-absent |
| `Switch` | `(T, List<Tuple<T, U>>, U) → U` | Switch expression |
| `Cond` | `(List<Tuple<Boolean, T>>, T) → T` | Conditional chain |

---

## 11. Presence and Missingness

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsAbsent` | `(T \| Absent) → Boolean` | Is absent |
| `IsPresent` | `(T \| Absent) → Boolean` | Is not absent |
| `AsAbsent` | `() → Absent` | Return absent |
| `OrElse` | `(T \| Absent, T) → T` | Default if absent |
| `MapIfPresent` | `(T \| Absent, T → U) → U \| Absent` | Transform if present |
| `FilterIfPresent` | `(T \| Absent, T → Boolean) → T \| Absent` | Filter if present |

---

## 12. Type Guards (General)

### 12.1 Scalar

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsBoolean` | `(Any) → Boolean` | Is Boolean |
| `IsText` | `(Any) → Boolean` | Is Text |
| `IsCharacter` | `(Any) → Boolean` | Is Character |

### 12.2 Numeric

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsNumber` | `(Any) → Boolean` | Is any number |
| `IsInteger` | `(Any) → Boolean` | Is Integer |
| `IsDecimalNumber` | `(Any) → Boolean` | Is DecimalNumber |
| `IsExponentialNumber` | `(Any) → Boolean` | Is ExponentialNumber |
| `IsPrecisionNumber` | `(Any) → Boolean` | Is PrecisionNumber |
| `IsFraction` | `(Any) → Boolean` | Is Fraction |
| `IsImaginaryNumber` | `(Any) → Boolean` | Is ImaginaryNumber |
| `IsComplexNumber` | `(Any) → Boolean` | Is ComplexNumber |
| `IsInfinity` | `(Any) → Boolean` | Is Infinity |

### 12.3 Collection

| Operator | Signature | Description |
|----------|-----------|-------------|
| `IsList` | `(Any) → Boolean` | Is List |
| `IsSet` | `(Any) → Boolean` | Is Set |
| `IsTuple` | `(Any) → Boolean` | Is Tuple |
| `IsMap` | `(Any) → Boolean` | Is Map |
| `IsRecord` | `(Any) → Boolean` | Is Record |
| `IsRange` | `(Any) → Boolean` | Is Range |

---

## 13. Codex Value Type Tokens

### 13.1 Scalar Tokens

| Token | Description |
|-------|-------------|
| `$Text` | Text value |
| `$Character` | Character value |
| `$Boolean` | Boolean value |

### 13.2 Numeric Tokens

| Token | Description |
|-------|-------------|
| `$Number` | Any numeric value |
| `$Integer` | Integer value |
| `$Zero` | Integer zero |
| `$NegativeInteger` | Negative integer |
| `$NonPositiveInteger` | Non-positive integer |
| `$NonNegativeInteger` | Non-negative integer |
| `$PositiveInteger` | Positive integer |
| `$DecimalNumber` | Number with decimal point |
| `$ExponentialNumber` | Number with exponent |
| `$PrecisionNumber` | Decimal with explicit precision |
| `$Fraction` | Fraction value |
| `$ImaginaryNumber` | Pure imaginary value |
| `$ComplexNumber` | Complex number |
| `$PositiveInfinity` | Positive infinity (`Infinity`) |
| `$NegativeInfinity` | Negative infinity (`-Infinity`) |
| `$Infinity` | PositiveInfinity or NegativeInfinity |

### 13.3 Temporal Tokens

| Token | Description |
|-------|-------------|
| `$ZonedDateTime` | Date, time, and timezone |
| `$Instant` | Absolute point in time with offset |
| `$PlainDateTime` | Date and time |
| `$PlainDate` | Calendar date |
| `$YearWeek` | ISO year and week |
| `$PlainYearMonth` | Year and month |
| `$PlainMonthDay` | Month and day |
| `$PlainTime` | Wall-clock time |
| `$Duration` | Length of time |
| `$TemporalKeyword` | `now` or `today` |

### 13.4 Color Tokens

| Token | Description |
|-------|-------------|
| `$Color` | Any color value (union of all color types) |
| `$HexColor` | Hexadecimal color (`#RGB`, `#RRGGBB`, etc.) |
| `$NamedColor` | Named color (`&red`, `&blue`, etc.) |
| `$RgbColor` | RGB color function (includes legacy `rgba()`) |
| `$HslColor` | HSL color function (includes legacy `hsla()`) |
| `$HwbColor` | HWB color function |
| `$LabColor` | CIE Lab color function |
| `$LchColor` | CIE LCH color function |
| `$OklabColor` | Oklab color function |
| `$OklchColor` | Oklch color function |
| `$ColorFunction` | Generic `color()` function |
| `$ColorMix` | `color-mix()` function |
| `$DeviceCmyk` | `device-cmyk()` function |

### 13.5 Identity Tokens

| Token | Description |
|-------|-------------|
| `$Uuid` | UUID value |
| `$IriReference` | IRI value |
| `$LookupToken` | Lookup token value |
| `$EnumeratedToken` | Schema-defined token |
| `$HostName` | Host name wrapper value |
| `$EmailAddress` | Email address wrapper value |
| `$Url` | URL wrapper value |

### 13.6 Collection Tokens

| Token | Description |
|-------|-------------|
| `$List` | List collection |
| `$Set` | Set collection |
| `$Map` | Map collection |
| `$Record` | Text-keyed map |
| `$Tuple` | Tuple collection |
| `$Range` | Range value |

**Parameterized forms:** `$List<T>`, `$Set<T>`, `$Map<K,V>`, `$Tuple<T1,T2,...>`, `$Range<T>`, `$Record<V>`

---

## 14. Error Behavior

All operators return `Validation<T>`:

- Domain violations → `Invalid([TypeMismatch, ...])`
- Division by zero → `Valid(Infinity)` or `Valid(-Infinity)` per operand sign
- `0 / 0` → `Valid(Infinity)` (not NaN, per Codex §5.4)
- `sqrt(-x)` where `x > 0` → `Valid(Infinity)` (not NaN)
- Empty collection access → `Valid(Absent)`
- Index out of bounds → `Valid(Absent)`

---

## 15. References

- `behavior-dialect-semantics/index.md` — Complete value model and coercion rules
- `behavior-dialect/index.md` — Evaluation model and type guards
- `behavior-vocabulary/math/index.md` — Mathematical operator definitions
- `behavior-vocabulary/text/index.md` — Text operator definitions
- `behavior-vocabulary/temporal/index.md` — Temporal operator definitions
- `behavior-vocabulary/core-safe-transforms/index.md` — Collection operator definitions
- `behavior-vocabulary/color/index.md` — Color operator definitions
- `behavior-vocabulary/identity/index.md` — Identity operator definitions
- `behavior-vocabulary/relational-and-predicates/index.md` — Relational operator definitions
- `behavior-vocabulary/presence-and-missingness/index.md` — Presence operator definitions
- `value-ordering-and-structural-equality/index.md` — Comparison semantics
- Codex Specification §5 — Value literal syntax
