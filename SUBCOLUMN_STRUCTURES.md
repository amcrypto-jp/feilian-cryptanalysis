# Deterministic XOR-difference structures of FEILIAN SubColumn

Mounir IDRASSI · Mathematical appendix to version 1.0.2 · 27 September 2026.

**For the specified 64-bit SubColumn, the four known MSB-only differences are the complete set of constant whole-output XOR derivatives, including when arbitrary 256-bit differences are allowed.** The classification follows from the universal identities below. It does not follow from sampling.

This mathematical appendix gives the SubColumn classification and composition limit used in R6 of the review. It concerns arbitrary inputs to the component equations shared by the specification and reference C. It establishes no collision, preimage or full-round security bound.

## Definitions and equations

Let N = 2^64 and M = N/2. Addition and subtraction below are modulo N. XOR is denoted by ⊕, and ROR is a 64-bit right rotation. For column input (a,b,c,d), write the component as

    p = a + b
    u = ROR8(d ⊕ p)
    v = c + d + Σ0(u)
    q = ROR63(b ⊕ v)
    SC(a,b,c,d) = (p + Σ1(q), q, v, u).

Here Σ0(z) = z ⊕ ROR5(z) ⊕ ROR48(z), and Σ1(z) = z ⊕ ROR11(z) ⊕ ROR40(z). The words are state rows 0,1,2,3.

For a vector-valued function F, define

    DδF(z) = F(z ⊕ δ) ⊕ F(z)
    LD(F) = {δ : DδF(z) is constant for all z}.

LD(F) is an F2-vector space: if DδF = ε and DηF = θ are constant, then D(δ⊕η)F = ε ⊕ θ. Restricting the output to one linear projection gives a weaker condition. All classification claims here concern the entire output vector.

## Lemma: constant XOR derivatives of two- and three-input addition

For a word width w ≥ 3, put N = 2^w and M = N/2. Let r be two or three. Suppose fixed masks α1,...,αr,β satisfy

    Σi (zi ⊕ αi) = (Σi zi) ⊕ β

for every independently varying tuple of words z1,...,zr. Then every αi belongs to {0,M}, and β is their XOR. Conversely, those masks satisfy the identity.

**Proof.** Let fa(z) = z ⊕ a. Setting every zi to zero gives β = Σi αi. Varying one coordinate at a time gives

    fαi(z) − αi = fβ(z) − β = g(z).

Varying two coordinates gives g(x+y) = g(x)+g(y). Thus g is an endomorphism of the cyclic additive group and g(z) = kz, where

    k = g(1) = (1 ⊕ β) − β ∈ {1,−1}.

If k = 1, fαi(z) = z+αi. Substitution z = αi gives 2αi = 0, so αi ∈ {0,M}. XOR by either of these masks is exactly addition by that mask.

If k = −1, fαi(z) = αi−z. Substitution z = N−1 gives 2αi = N−2, so αi is congruent to −1 modulo M. The same holds for β. But β = Σi αi would then require r ≡ 1 modulo M. This is impossible for r ∈ {2,3} and M ≥ 4. Thus only k = 1 remains. ∎

The width condition matters. At w = 2, a three-input sum also admits the k = −1 case. The checker explicitly verifies this small-width exception. Its small addition checks are tests of this arithmetic lemma, not reduced-width FEILIAN security experiments.

## Lemma: both Sigma maps are bijective

Represent a right rotation by t over F2[t]/(t^64+1). Since t^64+1 = (t+1)^64, a polynomial is invertible in this ring when it does not vanish at t = 1. The polynomials 1+t^5+t^48 and 1+t^11+t^40 both take value one there. Hence both Sigma maps are bijective.

This argument and the exact binary rank checks concern linear maps only. They impose no independence assumption on probabilistic differential propagation.

## T1: the four-element family

Define

    S = {(x,y,x,x⊕y) : x,y ∈ {0,M}}.

Then, for all base inputs,

    D(x,y,x,x⊕y) SC = (x⊕y,0,y,0).

**Proof.** XOR by M equals addition by M modulo N. The first two sums have differences x⊕y and y. The difference entering the rotation defining u cancels to zero. Consequently Σ0 contributes no difference, and v has difference y. The difference entering the rotation defining q also cancels to zero, so Σ1 contributes no difference. The final differences are (x⊕y,0,y,0). ∎

The Sigma differences cancel; the Sigma values themselves are not generally zero.

## T2: full classification

**Theorem.** For arbitrary 256-bit input differences,

    LD(SC) = S,    dim_F2 LD(SC) = 2.

**Proof of necessity.** Let an arbitrary difference (A,B,C,D) produce a constant whole-output derivative. No MSB restriction is assumed.

First inspect the final fourth word u. Its constant derivative implies that the derivative of p = a+b under (A,B) is constant: rotation is linear and the difference on d is the fixed word D. The two-input addition lemma therefore forces A,B ∈ {0,M}. Write P = A⊕B. It follows that

    Δp = P,    Δu = ROR8(D⊕P),    K = ΔΣ0(u) = Σ0(Δu).

Now inspect v = c+d+Σ0(u). The three unprimed summands vary independently. To see this, choose c,d and Σ0(u) arbitrarily; bijectivity of Σ0 determines u, then p = d⊕ROL8(u), and any choice of b determines a = p−b. Thus the three-input addition lemma applies to the fixed masks (C,D,K). It forces

    C,D,K ∈ {0,M},    Δv = C⊕D⊕K.

Since D,P are now MSB-only, Δu is either zero or 2^55. But

    Σ0(2^55) = 2^55 ⊕ 2^50 ⊕ 2^7,

which is neither zero nor M. Therefore Δu = K = 0 and D = P. Hence Δv = C⊕D.

For the final addition, set

    Q = Δq = ROR63(B⊕C⊕D),    J = ΔΣ1(q) = Σ1(Q).

The sequence of operations up to, but excluding, the final addition is a bijection on the four words: each addition, XOR update and rotation can be undone using the other current words. Its coordinates (p,q,v,u) therefore vary freely. Bijectivity of Σ1 makes p and Σ1(q) independent coordinates too. The two-input addition lemma forces J ∈ {0,M}.

Here B,C,D are MSB-only, so Q is either zero or **one**: ROR63(M) = 1. However,

    Σ1(1) = 1 ⊕ 2^53 ⊕ 2^24

is not MSB-only. Therefore Q = 0, so C = B⊕D = A. We have obtained exactly

    (A,B,C,D) = (A,B,A,A⊕B),    A,B ∈ {0,M}.

T1 gives sufficiency. ∎

The “independent coordinates” in this proof are a surjectivity statement about freely chosen component inputs. They are not a Markov assumption, a sampling assertion, or a claim that a hash caller can choose reachable internal states.

## T3–T4: matrix and row-permutation consequences

Let A denote the matrix operation consisting of four independent SubColumn calls, and R the specified row permutation. Because the four column inputs can vary independently, a whole-matrix derivative is constant exactly when each column derivative is constant. Thus

    LD(A) = S^4,    dim_F2 LD(A) = 8.

The output difference map sends column c's pair (xc,yc) to (xc⊕yc,0,yc,0). This is injective on S^4. Its image T is exactly the eight-dimensional space of MSB-only matrix differences supported in rows 0 and 2.

The row permutation is invertible and XOR-linear, so

    LD(R∘A) = S^4.

It permutes T onto itself. This concerns the output family T; it does not say that the input family S^4 is an invariant subspace.

## T5: the precise composition limit

**Theorem.** With H = R∘A,

    LD(A∘H) ∩ S^4 = {0}.

**Proof.** Take a nonzero δ ∈ S^4. T1–T4 give H(z⊕δ) = H(z)⊕ε with a nonzero ε ∈ T. Nonzero follows either from the explicit injective difference map or from bijectivity of H.

We have T∩S^4 = {0}: a member of S with its second and fourth words zero must have y = 0 and x⊕y = 0, hence x = 0. Therefore ε ∉ LD(A), by T3.

The remaining step needs surjectivity, not merely row support. Every SubColumn operation and R are bijective, so H ranges over the entire matrix state space. Consequently

    Dδ(A∘H)(z) = Dε A(H(z))

cannot be constant, since Dε A is nonconstant on that full space. ∎

Appending the final row permutation or XORing a common fixed constant does not change constancy. This excludes nonzero members of this family at the stated second-layer boundary. It does not classify differences outside S^4 for the complete round, prove the absence of high-probability behavior, or show that no longer composition can have a constant derivative.

## Computational checks and limits

[code/check_subcolumn_structures.py](code/check_subcolumn_structures.py) accompanies these proofs. It checks the arithmetic identities, exact binary ranks, the stated matrix difference map and finite nonconstancy certificates. With the hash-identified original submission, it also compares ordinary component evaluations against the scalar reference C.

Finding two different derivative values is an exact finite certificate that a particular candidate is not in LD(F). Conversely, obtaining one value on many samples does not prove membership. The universal positive claims and complete 64-bit classification depend on the proofs above. The checker is not a machine-checked proof of those arguments, and a successful exit does not authenticate arbitrary claims in its comments.

[The recorded results](evidence/subcolumn_structures.json) state the precise computational coverage. The small-width addition enumeration checks every candidate mask tuple, using a counterexample to reject each nonmember and all inputs to verify each member. There is no exhaustive enumeration of 256-bit SubColumn inputs or full-round hash analysis.

## Scope and background

The classification of constant whole-output derivatives of the complete round
outside S^4, projected-output structures and quantitative probability
dependencies remain separate questions. No IV-reachability,
compression-feedforward or digest-truncation claim follows from this appendix.
R1–R8 retain their stated scope and evidence classifications.

The whole-output condition is the binary vectorial translator notion studied
by Xuejia Lai in [Additive and linear structures of cryptographic
functions](https://doi.org/10.1007/3-540-60590-8_6). Lipmaa and Moriai study
[differential properties of modular addition](https://eprint.iacr.org/2001/001),
and Bao, Guo, Ling and Sasaki survey component criteria in
[SoK: Peigen](https://eprint.iacr.org/2019/209). These sources establish the
background; no exhaustive priority claim is made for this FEILIAN classification.
The review's assistance disclosure is in [AI_DISCLOSURE.md](AI_DISCLOSURE.md).
