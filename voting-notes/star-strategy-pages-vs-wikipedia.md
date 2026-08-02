# Our strategy education pages vs. Wikipedia's "Strategic voting"

Sources, all read 2026-08-01:

- [Q: Is STAR Voting vulnerable to strategic voting?](https://www.starvoting.org/strategic_voting) — the FAQ entry (three sentences)
- [Strategic STAR Voting?](https://equal.vote/strategic-star) — the substantive article, linked from the FAQ as "here"
- [Q: What if voter behavior isn't ideal under STAR Voting?](https://www.starvoting.org/voter_behavior)
- [Q: Will voters bullet vote with STAR Voting?](https://www.starvoting.org/bullet_voting)
- [Strategic voting § Cardinal single-winner voting](https://en.wikipedia.org/wiki/Strategic_voting#Cardinal_single-winner_voting) and [§ Common types of strategic voting](https://en.wikipedia.org/wiki/Strategic_voting#Common_types_of_strategic_voting)

Verifier for the two worked examples below: [code/star-strategy/verify.py](code/star-strategy/verify.py).

## The short version

The arguments hold up. The vocabulary, the sourcing, and one of the rebuttals don't.

STAR appears nowhere in Wikipedia's cardinal section — it covers score, approval, majority judgment, Borda, and positional voting — so there is no head-to-head to lose. What there is instead is a reader arriving from a densely footnoted encyclopedia article and landing on a three-sentence FAQ answer that cites nothing and names no strategy at all.

## Finding 1: our taxonomy is ours alone

The equal.vote article invents four category names. None of them appear in the literature or in Wikipedia:

| Ours | Standard term |
|---|---|
| Strong insincerity ("decapitation") | Compromise / lesser-evil / **favorite betrayal** |
| Weak insincerity ("skipping") | **Burial** |
| Restrictive sincerity ("tactical minimization") | **Compression** — truncation, bullet voting |
| Expansive sincerity ("tactical maximization") | Also compression — exaggeration |
| *not covered* | **Pushover / turkey-raising / raiding** |
| *not covered* | **Strategic abstention** |

Two consequences. Nobody searching "does STAR have a burial problem" reaches a heading called *Weak Insincerity*. And "restrictive **sincerity**" names a vote that is insincere by definition — to a reader coming from the literature it reads as an editing mistake, not a term of art.

Wikipedia also folds our third and fourth categories into one (compression), on the grounds that both are the same underlying move: refusing to disclose a preference, without any rank reversal. That merge is right, and finding 4 below shows it is *especially* right for STAR.

## Finding 2: uncited claims, where the citations exist

Every claim in Wikipedia's cardinal section carries a footnote — Balinski & Laraki 2010, Brams & Hershbach in *Science* 2001, and in the neighbouring section Green-Armytage 2014, Monroe 2001, Nagel 2007. Against that:

- [/voter_behavior](https://www.starvoting.org/voter_behavior) asserts "Peer Reviewed studies are clear that strategic voting in STAR Voting isn't effective or incentivised" and names none. The claim is defensible — [equal.vote/peer_review](https://www.equal.vote/peer_review) lists Wolk, Quinn & Ogren 2023 (*Constitutional Political Economy*) and Ogren 2023 (*Electoral Studies*) — but neither strategy page links to it.
- The 1:1 / 3:1 / 18:1 strategic-incentive ratios on equal.vote come from Quinn's Voter Satisfaction Efficiency work, which is a self-published simulation, not refereed. One screen below the words "peer reviewed," that blurs the two.
- Two dangling references: *"the authors of this paper call it 'decapitation'"* — no paper is linked anywhere on the page; and *"The Effect of Approval Balloting on Strategic Voting Under Alternative Decision Rules"* is named with no author, year, or link.

## Finding 3: one claim is refuted by our own notes

> "STAR Voting never encourages strong insincerity in balloting."

Two problems, one soft and one hard.

The soft one: the next two sentences describe a voter "highly motivated to send the stronger of the two to the runoff," which reads as conceding what the heading denies. That particular scenario isn't betrayal — you can score your favorite and your lesser evil both 5, and no reversal occurs.

The hard one: **"never" is false, and [star-voting.md](star-voting.md) already contains the counterexample.** Equal-rating is the usual escape hatch, so a genuine violation needs a case where equal-rating isn't enough — and exhaustive search over all 216 ballots for the manipulating bloc found one:

| Voters | A | B | C |
|---|---|---|---|
| 48 | 5 | 2 | 4 |
| 52 | 1 | 5 | 0 |
| 8 | 0 | 2 | 3 |

Sincerely, B wins and the 48-bloc gets a candidate worth 2 to them. *Every* ballot keeping A at or tied for the top is worth exactly 2, including A=5, C=5. Sinking their own favorite below C and bullet-voting C is worth 4. The mechanism is specific to STAR: their favorite A is strong enough to take the second runoff slot but not strong enough to win it, and while A occupies that slot, B wins. Nothing loyal works.

So the accurate claim is weaker and needs saying in our own voice before someone else says it for us: **equal-rating protects you in most cases, so you almost never have to rank a lesser evil above your favorite — but STAR fails favorite betrayal, partially, in cases where your favorite is too strong to eliminate and too weak to win.**

**Wikipedia makes the same mistake in our favor.** Its *Compromise* entry lists rated rules as *immune*, citing Green-Armytage 2014 at Proposition 4's note — a note that in fact lists approval and range among the methods *vulnerable* to compromising (see [wikipedia-talk-strategic-voting-draft.md](wikipedia-talk-strategic-voting-draft.md)). The paper defines compromising as giving a candidate the best possible ranking *or rating*, which in a rated method never requires demoting your favorite, and it never uses the term "favorite betrayal" at all. So both pages are erring on the same fault line: the intuition that equal-rating protects you is sound and is roughly what the source's definition implies, but neither "immune" nor "never" survives the cases where equal-rating isn't enough. Ours is the one we can fix.

That is not a concession we lack an answer to. [Farewell to Pass/Fail](https://www.equal.vote/pass_fail) is the answer: later-no-harm and favorite betrayal are an opposing pair, a method passing one absolutely fails the other badly (IRV passes later-no-harm, which is how center squeeze happens; approval passes favorite betrayal, which is what pushes voters to bullet vote), and STAR deliberately fails both a little. That argument is stronger than "never," and it's already written — it just isn't deployed on the strategy page, which is the one place a reader arrives already asking the question.

## Finding 4: the burial rebuttal has a precondition we don't state

This is the one that matters.

Our rebuttal to burial is that promoting a candidate you like less risks squeezing your own favorite out of the runoff, so it backfires. The article even cites the condition under which burial pays — the voter must believe their favorite can make the runoff, yet not be sure their favorite beats their second choice — and answers: "the voter who believes (3) cannot believe (1) with great confidence."

That answer holds when your favorite is *marginal* for the runoff. It does not hold when your favorite is comfortably first on score. And there is a second gap: at STAR's score cut only the *relative order* of totals matters, so the way to remove a strong rival is not to lower them — you may already have them at 0 — but to **lift a third candidate over them**. Our taxonomy files "lowering a rival" (weak insincerity) and "raising someone else" (expansive sincerity) as separate strategies with separate rebuttals, when at the cut they are the same move.

Verified, 7 voters, no tiebreaker anywhere (`verify.py`, example 2):

```
  voter |  A  B  C  D
      0 |  0  0  1  3
      1 |  1  2  5  3
      2 |  5  2  3  4
      3 |  3  4  2  4
      4 |  4  3  4  1
      5 |  2  5  0  2   <-- strategist
      6 |  4  5  5  1

  honest:    A 19  B 21  C 20  D 18   finalists B, C  ->  C wins
  strategic: voter 5 raises A from 2 to 4
             A 21  B 21  C 20  D 18   finalists A, B  ->  B wins
```

Voter 5 has C at 0 already and cannot bury them further. Raising A — a candidate they scored 2 — lifts A over C at the cut. C never reaches the runoff, A does and loses it, and voter 5 goes from their last choice winning to their favorite winning. Their favorite B led on score throughout and was never at risk, so the squeeze check never engaged.

This is an existence proof, not a frequency claim: it needs precise knowledge of where the cut will fall, and the simulation results we cite are about how rarely that pays off in practice. But "no advantage for it" is the wrong shape of claim, and a critic will build exactly this profile. The honest version — it requires information voters don't have, and misjudging the cut hands the election to the turkey — is both true and more persuasive.

### And STAR fails participation

Wikipedia lists point-summing systems as immune to strategic abstention. STAR is not purely point-summing, and the immunity does not transfer. Verified, 5 voters (`verify.py`, example 1):

```
  voter |  A  B  C  D
      0 |  4  5  0  2   <-- decides whether to show up
      1 |  0  5  5  0
      2 |  5  0  5  1
      3 |  0  4  0  5
      4 |  1  2  0  3

  stays home: A  6  B 11  C 10  D  9   finalists B, C  ->  B wins
  votes:      A 10  B 16  C 10  D 11   finalists B, D  ->  D wins
```

Voter 0's favorite B is in the runoff either way. Their two stars for D lift D over C, swapping the opponent — and the new opponent beats B. An honest ballot turned a 5-star winner into a 2-star one.

This is the participation-criterion form of the mechanism already documented as a later-no-harm failure in [star-voting.md](star-voting.md): support you give a middle candidate lifts them past the cut, and they then beat your favorite in the runoff. Same machinery, two different criteria — worth citing together rather than separately.

Nobody can exploit this deliberately, and the copy should say so. But it is the concrete form of the one open question Wikipedia poses about rated ballots — *"how highly to score their second-choice candidate"* — and our pages never answer it head-on, even though the runoff is the answer.

---

# Draft copy

## A. Terminology crosswalk — insert near the top of [equal.vote/strategic-star](https://equal.vote/strategic-star)

> ### What these strategies are called elsewhere
>
> Strategy names vary between the voting-reform literature, academic social choice, and general references like Wikipedia. This page uses the Equal Vote framing below; the standard terms are given alongside so you can follow the argument into the sources.
>
> | On this page | Also known as |
> |---|---|
> | Strong insincerity | Favorite betrayal, compromising, lesser-evil voting, decapitation |
> | Weak insincerity | Burial, burying, skipping |
> | Restrictive sincerity | Truncation, bullet voting, compression |
> | Expansive sincerity | Exaggeration, tactical maximization, min-maxing |
>
> Academic sources often group the last two together as **compression**, because both involve declining to show a preference rather than reversing one. Under STAR that grouping is apt: at the scoring cut only the relative order of totals decides who advances, so lowering one candidate and raising another are the same move seen from two directions.

Keeping our headings and adding the crosswalk costs nothing and makes every claim on the page traceable to the literature.

## B. New section — pushover

> ### Pushover ("turkey-raising")
>
> A pushover strategy means boosting a candidate you don't want to win, in order to knock a *stronger* rival out of contention, expecting the weak candidate to lose the final round anyway. It's a well-known problem for methods with elimination rounds, and it's why partisan primaries invite raiding.
>
> Score and approval voting are immune to it, because they have no elimination step at all. STAR has a single cut — the top two scores advance — so the honest answer is that STAR is not immune in that trivial sense, and it's worth being precise about what the strategy would require.
>
> To make it work, a voter would have to know, before any votes are counted, roughly where the second- and third-place scores will fall, and lift their chosen turkey across that line by the right margin. Overshoot and the turkey becomes the frontrunner. Misjudge the electorate and the turkey wins the runoff outright — and the strategist has handed the election to someone they specifically didn't want.
>
> That's the same wall every STAR strategy runs into: the runoff is decided by majority preference among all voters, not by scores, so a candidate you elevate can beat your favorite in the final round on strength you don't control. Simulation studies find these strategies close to break-even for the voter attempting them — roughly as likely to backfire as to pay off — compared with a 3:1 payoff under IRV and 18:1 under choose-one plurality.

## C. New section — abstention, and how high to score your second choice

> ### Should I abstain, or score my second choice lower?
>
> Some methods reward staying home. STAR doesn't reward it in any way a voter could act on: your ballot always counts as a full vote between the two finalists, whoever they turn out to be, so declining to vote gives up that vote for nothing.
>
> The real question voters ask is subtler, and it deserves a straight answer: **how high should I score my second choice?**
>
> The tension is genuine. Scoring your second choice high helps send them to the runoff — which is what you want if your favorite can't make it, and not what you want if your favorite can. There are constructed elections where a voter's honest, moderate support for a middle candidate lifts that candidate into the runoff against their favorite, and the middle candidate wins. No voting method escapes this kind of scenario, and we'd rather show it than pretend it away.
>
> What makes it a poor basis for strategy is that acting on it requires knowing where the cut will fall — and if you guess wrong in the other direction, you've withheld support from the candidate who ends up as your only defense against your last choice. Our guidance stands because it's robust to that uncertainty, not because the tension doesn't exist:
>
> - Give your favorite (or favorites) 5 stars.
> - Give your last choice 0.
> - Score everyone else to show your honest preference order and how strongly you feel.
>
> A ballot marked that way is never the *worst* available option for you, whatever the field turns out to look like. That is a stronger property than any strategy that depends on a correct guess.

## D. Rewritten FAQ answer for [/strategic_voting](https://www.starvoting.org/strategic_voting)

The current answer is three sentences, names no strategy, cites nothing, and hands off with link text "here". It's the page that ranks for "STAR voting strategic voting," so it's what a reader coming off the Wikipedia article hits first.

> **Q: Is STAR Voting vulnerable to strategic voting?**
>
> **A:** With STAR Voting, honesty is the best policy. Give your favorite or favorites a full 5 stars, give your last choice 0, and use the scores in between to show your honest preference order.
>
> No voting method eliminates strategic incentives entirely, so here's where the four main strategies stand under STAR:
>
> - **Favorite betrayal** (scoring a "lesser evil" *above* your true favorite): almost never necessary under STAR, because you can give both 5 stars — you're never forced to rank one over the other the way you are with a single-choice ballot. Constructed elections exist where equal scores aren't enough, and we don't claim otherwise; see [Farewell to Pass/Fail](https://www.equal.vote/pass_fail) for why we think a method that fails this criterion *slightly* beats one that passes it absolutely.
> - **Burial** (scoring a strong rival artificially low): the runoff blunts it. If burying a rival helps push your own favorite out of the top two, your full runoff vote goes to someone you like even less.
> - **Bullet voting** (scoring only your favorite): gives up your say in the runoff between everyone else. Across thousands of real STAR elections, voters overwhelmingly score multiple candidates.
> - **Exaggeration** (min-maxing everyone to 5s and 0s): the runoff makes it unnecessary. Every ballot counts as one full vote between the finalists no matter what scores it used.
>
> The catch for anyone hoping to game it: all of these need reliable advance knowledge of which two candidates will reach the runoff. Get that wrong and the strategy backfires. Simulation studies put STAR's strategic payoff at roughly break-even for the voter attempting it, against 3:1 under ranked choice voting and 18:1 under our current choose-one system.
>
> For the full analysis, see [Strategic STAR Voting?](https://equal.vote/strategic-star). For the underlying research, see our [peer-reviewed research page](https://www.equal.vote/peer_review).

## E. Citation fixes

1. Link [/peer_review](https://www.equal.vote/peer_review) from both [/strategic_voting](https://www.starvoting.org/strategic_voting) and [/voter_behavior](https://www.starvoting.org/voter_behavior), and replace bare "Peer Reviewed studies" with the two named papers (Wolk, Quinn & Ogren 2023, *Constitutional Political Economy*; Ogren 2023, *Electoral Studies*).
2. Label the 1:1 / 3:1 / 18:1 graphic as simulation results, with the study's year and a direct link, so it isn't read as one of the refereed findings.
3. Supply the "decapitation" paper — it's cited as "this paper" with nothing to click.
4. Supply author and year for "The Effect of Approval Balloting on Strategic Voting Under Alternative Decision Rules."
5. Replace link text "here" with the article title.

## Before publishing

- [ ] Confirm who coined "decapitation" and whether the paper is linkable, or drop the term.
- [ ] Confirm author/year for the approval-balloting paper.
- [ ] Have someone re-derive both worked examples independently (`verify.py` is a starting point, not a second opinion).
- [ ] Decide house position on finding 3. "Never encourages strong insincerity" is refuted by our own [star-voting.md](star-voting.md) counterexample; [Farewell to Pass/Fail](https://www.equal.vote/pass_fail) is the better answer and should be linked from the strategy page.
- [ ] Decide house position on finding 4 — the current "no advantage for it" wording will not survive a determined critic, and conceding the precondition costs little.
- [ ] Check whether the 18:1 / 3:1 / 1:1 figures match the current version of the VSE study, or an older one.

## On editing the Wikipedia article

The cardinal section's stated optimal strategy — top-rate everyone above average utility, bottom-rate the rest — is the approval-threshold result, and the whole STAR case is that a runoff breaks it. Wolk, Quinn & Ogren 2023 is a plausible source for a sentence on runoff-hybrid cardinal methods.

But we're affiliated, which makes this a [WP:COI](https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest) situation. Propose it on the article's talk page with the citation and let an uninvolved editor decide, rather than editing the section directly. An `{{edit COI}}` request on [Talk:Strategic voting](https://en.wikipedia.org/wiki/Talk:Strategic_voting) is the clean route.
