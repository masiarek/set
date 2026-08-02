# Errata email — *Math in Society* (Lippman), chapters 2–4

Companion to [math-in-society-lippman.md](math-in-society-lippman.md).

**Status: drafted, not sent.** Three errata plus a list of minor items. An earlier version carried a
fourth ask — that the chapter consider covering score voting — which stays cut; see *What stayed cut*
below.

## Where it goes

- **To: `dlippman@pierce.ctc.edu`** — David Lippman, Pierce College. Taken from
  [the book's own maintainer page](http://www.opentextbookstore.com/mathinsociety/), which asks that
  contributions be emailed to him. He is the author and the person who can change the text.
- **cc: `info@LibreTexts.org`** — named on the LibreTexts front matter for adoptions and adaptations.

Routing matters because LibreTexts is the **downstream** copy: every page carries *"authored, remixed,
and/or curated by David Lippman (The OpenTextBookStore) via source content that was edited to the
style and standards of the LibreTexts platform."* An erratum accepted only at LibreTexts leaves the
upstream book wrong, and one accepted only upstream leaves the LibreTexts copy wrong.

## The §2.14 item, and why it carries a disclosure

Item 3 is the §2.14 cutoff point. It is included as a **correction**, not a request: the claim is that
Example 13 does not demonstrate what it says it demonstrates, which is checkable in three lines of
arithmetic and true whatever anyone thinks of approval voting.

It still carries a one-sentence COI disclosure, for a reason worth being honest about: **the
correction happens to soften a criticism of a rated method**, and you have a connection to an
organisation promoting one. Someone who learned that later would think it relevant. Disclosed, it
costs a sentence; discovered, it discredits items 1 and 2 retroactively.

The disclosure is placed **at item 3, not at the top**. Items 1, 2 and 4 are method-neutral — item 2
is about apportionment and does not touch voting methods at all — and a header-level disclosure would
colour them for no reason.

Accept the tradeoff knowingly: the pure-errata version was a cleaner document. This one is more
useful and slightly more arguable.

## What stayed cut

The suggestion that the chapter add a section on score voting. Reasons unchanged:

1. It converts a correction into a request, which is a different kind of email.
2. It was not needed. The book is CC BY-SA 3.0 on a platform built for remixing — if chapter 2 should
   cover score voting, that can be done in a LibreTexts remix without anyone's permission, which is a
   better route than asking.
3. Item 3 already puts the interesting fact about cardinal ballots in front of him. If he takes it,
   the door is open on its own.

---

## The email

Subject: **Three errata in *Math in Society*, chapters 2–4**

---

Dear Professor Lippman,

I have been working through *Math in Society* chapters 2–4 in some detail, checking the worked
examples computationally as I went. Almost everything reproduces exactly — Nassau County, the Scottish
Parliament power indices, and the chapter 2 preference schedules all check out. Three statements do
not, and the first two are boxed theorem statements, which is why I thought they were worth writing to
you about.

**1. §2.12 states Arrow's theorem without the restriction to ranked methods, one page before approval
voting is introduced.**

The text reads:

> Arrow's Impossibility Theorem states, roughly, that it is not possible for a voting method to
> satisfy every fairness criteria that we've discussed.

Arrow's theorem applies to **ranked (ordinal)** methods. Its hypothesis is that the input is a profile
of rankings. Approval voting and other rated methods are not covered by it, because their ballots are
not rankings.

That would be a small thing, except for where it sits. §2.12 is titled "So Where's the Fair Method?"
and answers the chapter's running question with an impossibility result. §2.13 then introduces
approval voting. A student reading the sections in order has just been told that no voting method can
be fair, and then meets a method the theorem does not reach — with nothing in the text marking the
boundary. This is one of the more durable misconceptions in the area, and the sequencing here teaches
it directly.

The fix is one word:

> ...it is not possible for a **ranked** voting method to satisfy every fairness criteria that we've
> discussed.

A sentence at the top of §2.13 noting that approval voting takes a different kind of ballot, and so
falls outside the theorem just stated, would close it completely.

Two smaller points on the same page. The criteria named in the chapter — Condorcet, monotonicity,
majority, IIA — are not the conditions of Arrow's theorem, which are unrestricted domain, Pareto, IIA
and non-dictatorship; only IIA is shared, so the sentence attributes to Arrow something he did not
prove, even though the resulting claim is defensible. And the date given as 1949 is usually cited as
1950 (*Journal of Political Economy*) or 1951 (*Social Choice and Individual Values*).

**2. §4.4's statement of the Balinski–Young theorem includes a paradox that quota-satisfying methods
can avoid — and that Balinski and Young themselves showed how to avoid.**

The text reads:

> The Balinski-Young Impossibility Theorem shows that any apportionment method which always follows
> the quota rule will be subject to the possibility of paradoxes like the Alabama, New States, or
> Population paradoxes.

The theorem is that no method can satisfy the **quota rule** together with **population
monotonicity**. Satisfying quota while avoiding the **Alabama paradox** — house monotonicity — is
achievable. Balinski and Young constructed such a method themselves: the Quota method, *American
Mathematical Monthly* 82 (1975), 701–730. Still, *Mathematics of Operations Research* 4 (1979), 31–39,
characterises the full class of house-monotone methods satisfying quota.

The book's own exercise 9 makes this concrete. With populations 6000, 6000, 2000, Hamilton's method
gives (4, 4, 2) at ten seats and (5, 5, 1) at eleven — the Alabama paradox the exercise asks students
to identify, and Hamilton satisfies quota at both sizes. But

    (4, 4, 2) at ten seats  →  (5, 4, 2) at eleven seats

also satisfies quota at both sizes, and takes nothing away from anyone. So on the very instance the
chapter uses, following the quota rule does not force the paradox; Hamilton's particular remainder
rule does. I checked exhaustively that a quota-satisfying, house-monotone allocation exists at every
house size from 1 to 11 for this instance.

Suggested wording:

> The Balinski-Young Impossibility Theorem shows that any apportionment method which always follows
> the quota rule must be subject to the population paradox. In other words, we can choose a method
> that avoids the population paradox, but only if we are willing to give up the guarantee of
> following the quota rule.

**3. §2.14's majority-criterion failure is produced by an assumption about voters, not by approval
voting.**

A disclosure first, since unlike the other two items this one touches a method rather than a matter of
record: I am a volunteer contributor to software used by the Equal Vote Coalition, which advocates for
a rated voting method. Please weigh this item accordingly. It is a correction and not a request — I am
not asking that the chapter cover any additional method, and items 1, 2 and 4 stand independently of
it.

§2.14 opens "Approval voting can very easily violate the Majority Criterion," and Example 13
demonstrates it on:

     80 voters:  A > B > C
     15 voters:  B > C > A
      5 voters:  C > B > A

A holds a strict majority of first preferences, 80 of 100, and is also the Condorcet winner. The
demonstration then supposes that "every voter marked approval of their top two candidates," which
gives A 80, B 100, C 20, and elects B.

That supposition is doing all the work. On the same preference profile:

    approve top two (as supposed):  A 80,  B 100,  C 20   → B wins, majority criterion fails
    bullet vote:                    A 80,  B  15,  C  5   → A wins, majority criterion holds
    approve all three:              A 100, B 100, C 100   → no winner at all

Same preferences, same tabulation rule, three different outcomes. So Example 13 does not show that
approval voting violates the majority criterion; it shows that approval voting *together with a
particular cutoff rule* does.

This is a real and well-studied feature of approval rather than an oversight in the example: the
tabulation is fixed but the ballot is not, so many of approval's criterion compliances are properties
of voter behaviour rather than of the method. Saari and Van Newenhizen (*Public Choice* 59, 1988) make
it a formal result; Brams reads the same fact as a virtue rather than a defect.

The opening sentence is not wrong — approval *can* fail the majority criterion. The issue is that the
example as written invites a student to attribute to the method something the supposition supplied. A
clause would fix it: noting that the outcome depends on where voters set their cutoff, and that these
same voters bullet-voting would elect A, is a more interesting lesson than the one currently drawn and
costs about a sentence.

**4. Three smaller things, take or leave.**

- §4.2 says Hamilton's method "was approved by Congress in 1791, but was vetoed by President
  Washington." The bill passed the House on 21 February 1792 and the Senate on 12 March 1792, and
  Washington's veto — the first in US history — was 5 April 1792. §4.3 then says Jefferson's method
  was "used in Congress from 1791 through 1842"; the replacement act was signed 14 April 1792.
- §3.4's Scottish Parliament example gives [65: 47, 46, 17, 16, 2], which totals 128. The Scottish
  Parliament has 129 seats; the 2007 election also returned one independent, Margo MacDonald. The
  example's point survives restoring her — the Liberal Democrats and the Greens still have equal
  Banzhaf power — but she is not a dummy: she is critical in two winning coalitions, holding 1/28 of
  the power, which is somewhat more than a third of what the 16-seat Liberal Democrats hold.
- §3.2 says in the definition box that the quota must be *more than* half the total weight, then a
  line later that "the quota must be at least half the total number of votes." The book's own example,
  [3: 3, 2, 1], is the counterexample to "at least" — quota 3 is exactly half of 6, and that is
  precisely the case the paragraph is explaining why to exclude.

Thank you for the book, and for keeping it open — being able to check the examples against the live
text is the only reason I could write any of this. I am happy to send the verification script if it
would be useful, and equally happy to be told I have misread something.

Best regards,

Adam Masiarek
