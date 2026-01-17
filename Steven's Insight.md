# 📞 Research Debrief: Time Series Concepts for Capacity Planning

> **Date:** January 16, 2026  
> **Context:** Phone conversation with a friend who researched time series strategies for the ICPE 2026 Shaved Ice project  
> **Translation Layer:** All concepts are framed through the lens of retail inventory management → cloud VM capacity

---

## The Big Picture (Before We Dive In)

Think of this like managing inventory at a store, except instead of products on shelves, we're managing **virtual machines (VMs)** in the cloud. Too few VMs? The system crashes (like running out of stock). Too many VMs? We're paying for servers that sit idle (like overstock gathering dust in the back room).

---

## 1. The Rolling Average Buffer Strategy

### What Your Friend Said:
*"Rolling average with a 5,000 buffer based on the variance."*

### What This Means (Retail Analogy):
Imagine you sell ice cream. You don't just look at how many cones you sold *today*—you look at the **last 7 days** to get a sense of your typical demand. That's a **rolling average**: a moving calculation that always looks at the most recent window of time.

**The 5,000 buffer** is like your safety stock. If your rolling average says you need 10,000 VMs, you actually provision 15,000 (10,000 + 5,000 buffer) just in case demand spikes.

### How It Connects to Your Project:
In `MASTER_PROJECT.md`, you already identified the formula:
```
total_capacity = demand_7d_avg + safety_stock_95pct
```

The "5,000 buffer" your friend mentioned is essentially the **safety stock** component. The key insight: this buffer should be **based on variance**, not just a flat number. If demand is volatile (high variance), you need a bigger buffer. If it's stable (low variance), a smaller buffer is fine.

---

## 2. The Asymmetric Cost of Errors

### What Your Friend Said:
*"Crashing gets us a high net loss versus committing a bit more to be safe... doesn't matter if we commit too high as long as we have a net gain."*

### What This Means (Retail Analogy):
Think about what hurts more:
- **Under-stock (ran out):** Angry customers, lost sales, reputation damage. The cost is HIGH.
- **Over-stock (had too much):** Some extra inventory cost, maybe a discount sale. The cost is LOWER.

It's the same with VMs:
- **Under-provision (not enough VMs):** System crashes. Users can't access the service. Emergency scrambling. **This is expensive.**
- **Over-provision (too many VMs):** We pay for idle servers. Not great, but manageable. **This is cheaper than crashing.**

### The Insight:
Your friend is saying: **It's better to slightly over-commit than to be caught with nothing when demand spikes.** If you provision a little extra and the spike doesn't happen, you lose some money on unused VMs. But if you *don't* provision extra and the spike *does* happen, you lose a lot more.

### How It Connects to Your Project:
This is exactly the cost trade-off in `MASTER_PROJECT.md`:
```
        Low Buffer                    High Buffer
           ↓                              ↓
     More Stockouts              Less Stockouts
     Lower Holding Cost          Higher Holding Cost
```

Your goal is to find where the cost lines cross. But your friend's insight adds: **the lines aren't equal**. The cost of under-provisioning (downtime) is usually MUCH higher than over-provisioning (idle VMs).

---

## 3. The Insurance Model (Tracking/Commitment)

### What Your Friend Said:
*"Sell something to a buyer, pay for insurance... how much are you okay with if it goes wrong? If it's $100 worst case, $100 is covered. Or if it was $40 and they lose tracking before you have to commit more—buying tracking, commit to buying insurance which is like having more active VMs."*

### What This Means (Retail Analogy):
Imagine you're shipping a package to a customer:
- **No insurance, no tracking:** Cheapest option. But if the package gets lost, you're fully on the hook.
- **Tracking only ($5):** You can see where it is. You know *when* to worry.
- **Full insurance ($20):** If anything goes wrong, you're covered.

The question: How much **risk** are you willing to accept?

For VMs:
- **Minimal provisioning:** Cheapest, but if demand spikes, you crash.
- **Some buffer (tracking):** You can *see* demand building and react.
- **Large buffer (insurance):** You're covered no matter what happens.

### The Insight:
"Buying insurance" = **keeping extra VMs on standby**. The cost of that insurance is the price of those idle VMs. But if the "worst case" happens (a huge demand spike), you're protected.

### How It Connects to Your Project:
Your safety stock calculation (`safety_stock_95pct`) is literally the "insurance" amount. The 95th percentile means: "I'm covered 95% of the time." You can tune this—want 99% coverage? Buy more insurance (bigger buffer). Okay with 90%? Cheaper insurance (smaller buffer).

---

## 4. Accepting Small Losses

### What Your Friend Said:
*"It's okay to take a loss if it's minuscule, but if you don't commit and you don't have enough VMs, you need enough in case the worst case happens."*

### What This Means (Retail Analogy):
Let's say you're selling concert T-shirts:
- Occasionally you sell 1 or 2 fewer than you stocked. You're stuck with 2 extra shirts. **Minor loss. Acceptable.**
- But the one time 500 fans show up and you only have 100 shirts? **Massive loss. Unacceptable.**

### The Insight:
Small, frequent losses are tolerable. Rare, catastrophic losses are not. This is why you plan for the **worst case**—even if it doesn't happen most of the time.

### How It Connects to Your Project:
Your `mart_stockout_events` table tracks when demand exceeded capacity. Those are the "catastrophic" events. Even if they're rare, they're the ones causing real damage.

---

## 5. The 7-Day Rolling Average Explained

### What Your Friend Said:
*"7-day rolling average—like shifting a window. Jan 1-7: if we want an average, we look at those 7 days. For Jan 8, we look at Jan 2-8, forget Jan 1 for a bit. As it does that, we're always tracking 5 weekdays and 2 weekends."*

### What This Means (Simple Breakdown):

A **rolling average** is a "sliding window" calculation. Here's a visual:

```
Date        | Demand | 7-Day Window      | Rolling Average
------------|--------|-------------------|----------------
Jan 1       | 100    | (not enough data) | N/A
Jan 2       | 120    | (not enough data) | N/A
Jan 3       | 110    | (not enough data) | N/A
Jan 4       | 130    | (not enough data) | N/A
Jan 5       | 140    | (not enough data) | N/A
Jan 6       | 90     | (not enough data) | N/A
Jan 7       | 80     | Jan 1-7           | 110 (average of 7 days)
Jan 8       | 150    | Jan 2-8           | 117 (window slides forward)
Jan 9       | 160    | Jan 3-9           | 123 (window slides again)
```

Each day, the "window" slides forward by one day. You always include the **most recent 7 days**, dropping the oldest one.

### Why 7 Days Specifically?
Your friend explained: a 7-day window **always captures 5 weekdays + 2 weekend days**. This is important because:
- **Weekday demand:** Higher (everyone's working, services are in use)
- **Weekend demand:** Lower (fewer users)

If you used a 5-day window, some weeks you'd only see weekdays, making your average artificially high. A 7-day window smooths out this weekly cycle.

### How It Connects to Your Project:
In your Day 2 action plan, you were already planning to compute:
```python
df['rolling_std_7d'] = df.groupby(['region', 'instance_type'])['demand'].transform(
    lambda x: x.rolling(7).std()
)
```

This calculates the **rolling standard deviation** (a measure of variance) over the same 7-day window. The rolling *average* tells you "What's typical?" The rolling *standard deviation* tells you "How much does it fluctuate?"

---

## 6. Why Mean, Not Median?

### What Your Friend Said:
*"It's fine to use the mean. VMs are volatile. If you use the median and there was a spike, you'd never see it in the median—it doesn't tell you anything. Mean is representative of the real-world volatility."*

### What This Means (Simple Breakdown):

**Mean (Average):** Add all values, divide by count. Sensitive to spikes.
**Median:** The middle value when sorted. Ignores spikes.

Example:
```
Demand over 7 days: 100, 100, 100, 100, 100, 100, 500 (spike on day 7)

Mean = (100 + 100 + 100 + 100 + 100 + 100 + 500) / 7 = 157
Median = 100 (the middle value if you line them up)
```

The **median** completely ignores that day 7 spike. The **mean** gets pulled up by it.

### The Insight:
For capacity planning, **you WANT to see the spikes**. The spikes are what cause crashes! If you use the median, you'd plan for 100 VMs... and then day 7 hits with 500 demand and you're dead.

### How It Connects to Your Project:
This validates why your `mart_forecast_input` model should use mean-based aggregations, not median. The variance (which captures those spikes) is the whole point of your research question.

---

## 7. The Weekend Dip Pattern

### What Your Friend Said:
*"Always be tracking the dips that come from the weekend. With VMs, we expect peak demand during weekdays and it dips during the weekend—that affects the mean by a lot."*

### What This Means (Retail Analogy):
Think about a coffee shop:
- **Monday-Friday:** Busy. Office workers need caffeine.
- **Saturday-Sunday:** Slower. People sleep in.

If you staffed your coffee shop based on the weekly average, you'd:
- Be **understaffed** on Tuesday at 8am (peak)
- Be **overstaffed** on Sunday at 7am (slow)

VMs work the same way. Business applications = weekday peaks. The weekend dip drags down your overall average.

### The Insight:
You can't just look at "the overall average"—you need to understand the **cyclical pattern** (weekly seasonality). The 7-day rolling average helps smooth this out, but you should also:
1. **Track weekday vs. weekend separately** (maybe add a `is_weekend` flag)
2. **Don't over-react to weekend dips** (they're expected, not anomalies)

### How It Connects to Your Project:
Your Day 2 action plan already includes:
> "Add day-of-week encoding | Weekday/weekend patterns drive demand"

This is exactly what your friend was describing. Consider adding:
```python
df['is_weekend'] = df['date'].dt.dayofweek >= 5  # Saturday=5, Sunday=6
```

---

## 8. The "Let It Go" Rule

### What Your Friend Said:
*"Consider a 7-day average. If the overall average is not that great, we can let it go."*

### What This Means:
If the 7-day rolling average shows consistently low demand (maybe there's a holiday week, or a temporary slowdown), you don't need to keep massive capacity standing by. **Let some resources go** (scale down).

### The Insight:
This is about **dynamic scaling**. You shouldn't hold onto maximum capacity forever. If your rolling average shows a sustained decrease, it's safe to scale down.

### How It Connects to Your Project:
This might be relevant to the **structural break** you discovered in mid-2022 (possible client departure). After the break:
- Demand dropped significantly
- The old capacity levels became unnecessary
- The system should have "let go" of some VMs

---

## Summary: Action Items for Your Project

| Insight | What To Do |
|---------|------------|
| Rolling average buffer | Implement `demand_7d_avg + safety_stock_95pct` as your capacity formula |
| Asymmetric costs | Weight under-provisioning errors higher than over-provisioning in your cost function |
| Insurance model | Frame safety stock as "insurance premium"—how much are you willing to pay for protection? |
| Accept small losses | Don't optimize for zero waste; optimize for "no catastrophes" |
| 7-day window | Ensures you always capture the weekday/weekend cycle |
| Mean over median | Use mean to preserve visibility of demand spikes |
| Weekend dips | Add `is_weekend` flag for day-of-week analysis |
| "Let it go" | Design for dynamic scaling when sustained low demand is detected |

---

## Glossary: Terms You Heard Today

| Term | Plain English | Math/Code |
|------|---------------|-----------|
| **Rolling Average** | A moving window that calculates the average of the most recent N days | `df['demand'].rolling(7).mean()` |
| **Rolling Standard Deviation** | Same window, but measures how much values fluctuate | `df['demand'].rolling(7).std()` |
| **Variance** | How spread out your data is from the average | `std ** 2` |
| **Buffer / Safety Stock** | Extra capacity you hold "just in case" | `demand_avg + buffer` |
| **Asymmetric Cost** | When one type of error is much more expensive than another | Under-provision > Over-provision |
| **Weekday/Weekend Seasonality** | The predictable weekly cycle of high/low demand | 5 busy + 2 slow days |

---

*This transcript was reconstructed from conversation notes on January 16, 2026.*
