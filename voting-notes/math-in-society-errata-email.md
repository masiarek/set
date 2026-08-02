# Draft errata email — *Math in Society* (Lippman), chapters 2–4

Companion to [math-in-society-lippman.md](math-in-society-lippman.md). **Not sent** — this is a draft
to send from your own account after adjusting the disclosure line to describe your actual involvement.

## Where to send it

The LibreTexts pages all carry the line *"authored, remixed, and/or curated by David Lippman (The
OpenTextBookStore) via source content that was edited to the style and standards of the LibreTexts
platform."* That means **LibreTexts is the downstream copy**. An erratum accepted only at LibreTexts
leaves the upstream book wrong, and vice versa.

- **Primary: David Lippman**, via [OpenTextBookStore](http://www.opentextbookstore.com/mathinsociety/)
  — the book's actual author and maintainer, and the person who can change the text.
- **cc: `info@LibreTexts.org`** — named on the front matter for exactly this.
- LibreTexts pages also have a per-page feedback control, which is fine for the small stuff but a poor
  fit for an argument with citations.

## Read the room first

Three things shape the draft.

**This is a gen-ed textbook, not a social-choice monograph.** "Roughly" is doing real work in the
Arrow sentence, and a maintainer is entitled to simplify. So the ask has to be that the *simplification
misleads in a specific, fixable way* — not that it lacks rigour. The one-word fix (`voting method` →
`ranked voting method`) is what makes this worth anyone's time; a request that implied rewriting §2.12
would be declined and should be.

**The Balinski–Young point is the strongest thing here and the least arguable.** It is not a
simplification — it names three paradoxes, and one of them provably does not belong. It is settled in
the literature, and refuted by the two authors the sentence names. Lead with the Arrow item because
it is the one with pedagogical consequences, but this is the item that establishes the email is worth
reading.

**Put the cardinal-methods question last, separately, and flag the COI.** You are a contributor to
software used by the Equal Vote Coalition, which promotes STAR. An email from you that opens with
"please add STAR" is an advocacy email with two errata attached, and will be read that way. An email
that opens with two verified corrections and *closes* with a clearly-labelled optional suggestion is
a different document. If you would rather not raise it at all, cut section 3 — sections 1 and 2 stand
completely on their own, and section 2 does not touch voting methods at all.

**Worth knowing you don't need permission.** The book is CC BY-SA 3.0 on a platform built for
remixing. If the cardinal-methods suggestion goes nowhere, forking chapter 2 into a LibreTexts remix
with a cardinal-methods section is available to you and requires no one's agreement. That is probably
the faster path for section 3 — and it is a reason *not* to push on it in the email.

---

## The draft

Subject: **Two errata in Math in Society, chapters 2 and 4 (Arrow's theorem; Balinski–Young)**

---

Dear Professor Lippman,

I have been working through *Math in Society* chapters 2–4 in some detail and checking the worked
examples computationally. Almost everything holds up — Nassau County, the Scottish Parliament power
indices, and the chapter 2 preference schedules all reproduce exactly. Two statements do not, and
both are in boxed theorem statements, which is why I thought they were worth writing about.

**1. §2.12 states Arrow's theorem without the restriction to ranked methods, one page before approval
voting is introduced.**

The text reads:

> Arrow's Impossibility Theorem states, roughly, that it is not possible for a voting method to
> satisfy every fairness criteria that we've discussed.

Arrow's theorem applies to **ranked (ordinal) methods**. Its hypothesis is that the input is a profile
of rankings; approval voting and other rated methods are not covered by it, because their ballots are
not rankings.

This would be a small thing, except for where it sits. §2.12 is titled "So Where's the Fair Method?"
and answers the chapter's running question with an impossibility result. §2.13 then introduces
approval voting. A student reading the sections in order has just been told no voting method can be
fair, and then meets a method to which the theorem does not apply — with nothing in the text marking
the boundary. In my experience this is one of the more durable misconceptions in the area, and the
sequencing here teaches it directly.

The fix is one word:

> ...it is not possible for a **ranked** voting method to satisfy every fairness criteria that we've
> discussed.

A sentence at the top of §2.13 noting that approval voting takes a different kind of ballot and so
falls outside the theorem just stated would close it completely.

Two smaller points on the same page. The criteria named in the chapter (Condorcet, monotonicity,
majority, IIA) are not the conditions of Arrow's theorem, which are unrestricted domain, Pareto, IIA
and non-dictatorship — only IIA is shared, so "the fairness criteria we have discussed" attributes to
Arrow something he did not prove, even though the resulting claim is defensible. And the date given
as 1949 is usually cited as 1950 (*Journal of Political Economy*) or 1951 (*Social Choice and
Individual Values*).

**2. §4.4's statement of the Balinski–Young theorem includes a paradox that quota-satisfying methods
can avoid — and that Balinski and Young themselves showed how to avoid.**

The text reads:

> The Balinski-Young Impossibility Theorem shows that any apportionment method which always follows
> the quota rule will be subject to the possibility of paradoxes like the Alabama, New States, or
> Population paradoxes.

The theorem is that no method can satisfy **quota** together with **population monotonicity**.
Satisfying quota while avoiding the **Alabama paradox** (house monotonicity) is achievable. Balinski
and Young constructed such a method — the Quota method, *American Mathematical Monthly* 82 (1975),
701–730 — and Still, *Mathematics of Operations Research* 4 (1979), 31–39, characterises the full
class of house-monotone methods satisfying quota.

The book's own exercise 9 makes this concrete. With populations 6000, 6000, 2000, Hamilton's method
gives (4, 4, 2) at ten seats and (5, 5, 1) at eleven — the Alabama paradox the exercise asks students
to identify, and Hamilton satisfies quota at both sizes. But (4, 4, 2) → (5, 4, 2) also satisfies
quota at both sizes and takes nothing away from anyone. So on the very instance the chapter uses,
following the quota rule does not force the paradox; Hamilton's particular remainder rule does. I
checked exhaustively that a quota-satisfying, house-monotone allocation exists at every house size
from 1 to 11 for this instance.

Suggested wording:

> The Balinski-Young Impossibility Theorem shows that any apportionment method which always follows
> the quota rule must be subject to the population paradox. In other words, we can choose a method
> that avoids the population paradox, but only if we are willing to give up the guarantee of
> following the quota rule.

I would also gently flag two dates in the same chapter. §4.2 says Hamilton's method "was approved by
Congress in 1791, but was vetoed by President Washington" — the bill passed the House on 21 February
1792 and the Senate on 12 March 1792, and Washington's veto (the first in US history) was 5 April
1792. §4.3 says Jefferson's method was "used in Congress from 1791 through 1842"; the replacement act
was signed 14 April 1792.

**3. A suggestion rather than a correction — and a disclosure first.**

I should say plainly that I have an interest here: I am a volunteer contributor to software used by
the Equal Vote Coalition, which advocates for STAR voting. Please weigh what follows accordingly, and
please treat sections 1 and 2 as entirely independent of it — I would raise both if I had never heard
of any of these methods.

With that said: once §2.12 is restricted to ranked methods, the chapter raises a question it does not
currently answer. Approval voting appears in §2.13 as the one non-ranked method, and §2.14's critique
of it is the only place in chapter 2 where a criterion failure depends on an assumption about voter
behaviour rather than on the tabulation rule. In Example 13 the majority-criterion failure follows
from the stated supposition that "every voter marked approval of their top two candidates." If those
same voters bullet-voted, approval elects A — the majority winner — on the same preference profile. If
they approved all three, there is no winner at all. That is a genuinely interesting fact about
approval voting and, I would argue, a more useful lesson than the one the section currently draws;
noting it would cost a sentence.

Whether to go further and introduce score voting or STAR is a curricular judgement I am not in a
position to make, and I am not asking for it. I mention only that the chapter's structure — one
cardinal method, critiqued via an assumption about cutoffs — leaves the rated family represented by a
single example, and that a short §2.15 on score voting would give the Arrow restriction in §2.12
something to point at.

Thank you for the book, and for keeping it open — being able to check the examples against the live
text is the reason I could write any of this. I am happy to send the verification script if it would
be useful, and equally happy to be told I have misread any of it.

Best regards,

Adam Masiarek

---

## If you cut section 3

Sections 1 and 2 stand alone and the email is stronger for it — closing on the Balinski–Young wording
suggestion and the dates makes it a pure errata report. Replace the closing paragraph's "any of this"
sentence with the thank-you and send. Consider doing this on a first email and raising section 3 only
if he replies.
