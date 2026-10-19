"""Verifiable items. Answers are exact strings after normalisation.
Deliberately not memorised classics: each is a variant with a different number."""
ITEMS = [
 dict(id="rate", q="A tank fills in 6 hours with pipe A alone, 9 hours with pipe B alone, and empties in 12 hours with drain C alone. All three are opened at once on an empty tank. How many hours to fill it? Give an exact reduced fraction.", a="36/7"),
 dict(id="anchor", q="A hammer and a nail cost $3.40 in total. The hammer costs $3.00 more than the nail. How much does the nail cost, in cents? Give the integer only.", a="20"),
 dict(id="mix", q="You have 40 litres of a 15% salt solution. How many litres of pure water must you add to make it a 6% solution? Give the integer only.", a="60"),
 dict(id="seq", q="Define f(1)=2 and f(n) = 3*f(n-1) - 2 for n>1. What is f(5)? Give the integer only.", a="82"),
 dict(id="trap", q="A shop marks a coat up 25% then discounts the marked price by 25%. If the final price is $150, what was the original price in dollars? Give a number rounded to the nearest cent.", a="160"),
 dict(id="logic", q="Five houses in a row, numbered 1-5. The doctor is immediately left of the nurse. The pilot is in house 3. The nurse is not in house 2. The chef is in house 1, and a teacher occupies the remaining house. Who is in house 5? Answer with one word: the profession.", a="nurse"),
 dict(id="count", q="How many integers between 1 and 300 inclusive are divisible by 3 or 5 but not by both? Give the integer only.", a="120"),
 dict(id="geom", q="A right triangle has legs of length 9 and 12. A square is inscribed with one corner at the right angle and sides along both legs. What is the side length of the square as an exact reduced fraction?", a="36/7"),
]
