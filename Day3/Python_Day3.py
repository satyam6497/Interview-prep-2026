import pandas as pd


# =================================================================
# LOAD DATA
# =================================================================

orders = pd.read_csv("olist_orders_dataset.csv",parse_dates=["order_purchase_timestamp","order_delivered_customer_date","order_estimated_delivery_date"])

customers = pd.read_csv("olist_customers_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
payments = pd.read_csv("olist_order_payments_dataset.csv")


# =================================================================
# PART 1: DELIVERY PERFORMANCE
# =================================================================

# TODO: what % of orders have order_status == 'delivered'?

pct_delivered = round(((orders['order_status'] == 'delivered').sum() / len(orders)) * 100,2)

# print(f"% of orders delivered: {pct_delivered}%")


# TODO: of DELIVERED orders, what % were delivered ON TIME?

delivered = orders[orders['order_status'] == 'delivered']

pct_ontime_orders = round(((delivered['order_delivered_customer_date']<= delivered['order_estimated_delivery_date']).sum()/ len(delivered)) * 100,2)

# print(f"% of delivered orders that were on time: {pct_ontime_orders}%")


# TODO: what's the average delivery delay in days,
# for orders delivered LATE?

orders['delivery_delay'] = (orders['order_delivered_customer_date']- orders['order_estimated_delivery_date']).dt.days

avg_delay = orders.loc[orders['delivery_delay'] > 0,'delivery_delay'].mean()

# print(f"Average delay for late orders: {round(avg_delay, 2)} days")


# =================================================================
# PART 2: REPEAT CUSTOMER RATE
# (customer_id vs customer_unique_id gotcha)
# =================================================================

# TODO: merge orders with customers to bring
# customer_unique_id onto each order

Table1 = pd.merge(orders,customers,how="inner",on="customer_id")


# TODO: count orders per customer_unique_id
# NOT per customer_id

orders_per_customer = (Table1.groupby('customer_unique_id')['order_id'].count())


# TODO: what % of unique customers placed more than 1 order?

repeat_customers = (orders_per_customer > 1).sum()

pct_repeat_customers = round(repeat_customers / len(orders_per_customer) * 100,2)


# Wrong approach: group by customer_id

orders_per_customer_wrong = (Table1.groupby('customer_id')['order_id'].count())

repeat_customers_wrong = (orders_per_customer_wrong > 1).sum()

pct_repeat_customers_wrong = round(repeat_customers_wrong / len(orders_per_customer_wrong) * 100,2)


# print(f"\nCorrect % of repeat customers: {pct_repeat_customers}%")
# print(f"Wrong % of repeat customers: {pct_repeat_customers_wrong}%")


# =================================================================
# PART 3: REVENUE / ORDER VALUE ANALYSIS
# =================================================================

# TODO: merge order_items with orders
# Note: an order can have multiple items/rows
# Sum price + freight_value per order_id first.

Table2 = pd.merge(orders,order_items,how="inner",on="order_id")


# Calculate value for each item row

Table2['item_value'] = (Table2['price'] +Table2['freight_value'])


# Sum item values to get total order value

order_values = (Table2.groupby('order_id')['item_value'].sum().reset_index(name='total_order_value'))


# TODO: what's the average order value?
# What does the distribution look like?

avg_order_value = order_values['total_order_value'].mean()

# print(f"\nAverage Order Value: "f"{round(avg_order_value, 2)}")


# print("\nOrder Value Distribution:")
# print(order_values['total_order_value'].describe())


# print("\nOrder Value Quantiles:")
# print(order_values['total_order_value'].quantile([0.5, 0.9, 0.99]))


# TODO: do repeat customers spend more on average per order
# than one-time customers?

order_customer_values = pd.merge(order_values,Table1[['order_id', 'customer_unique_id']],on='order_id',how='inner')


# Count total orders for each unique customer

customer_order_counts = (order_customer_values.groupby('customer_unique_id')['order_id'].count())


# Assign customer type to every order

order_customer_values['customer_type'] = (order_customer_values['customer_unique_id'].map(customer_order_counts).apply(lambda x: 'Repeat'if x > 1 else 'One-time'))


# Compare average order value

avg_order_value_by_type = (order_customer_values.groupby('customer_type')['total_order_value'].mean())


print("\nAverage Order Value by Customer Type:")
print(avg_order_value_by_type.round(2))


# =================================================================
# PART 4: GEOGRAPHY
# =================================================================

# TODO: which customer_state has the most orders?

orders_by_state = (
    Table1.groupby('customer_state')['order_id'].count().sort_values(ascending=False)
)


print("\nOrders by State:")
print(orders_by_state)


print(f"\nState with most orders: "f"{orders_by_state.index[0]}")

print(f"Number of orders: "f"{orders_by_state.iloc[0]}")


# TODO: does delivery delay vary meaningfully by state?

late_state_delay = (
    Table1[Table1['delivery_delay'] > 0].groupby('customer_state')['delivery_delay'].mean().sort_values(ascending=False)
)

print(late_state_delay.round(2))


print("\nAverage Delivery Delay by State:")
print(late_state_delay.round(2))


print("\nTop 5 States by Average Delivery Delay:")
print(
    late_state_delay.head(5).round(2)
)


print("\nBottom 5 States by Average Delivery Delay:")
print(
    late_state_delay.tail(5).round(2)
)


# =================================================================
# PART 5: WRITE THE INSIGHT
# =================================================================

# The analysis shows that 97.02% of orders were delivered, with 91.88% of delivered orders arriving on time. Only 3.12% of unique customers were repeat customers,
# and repeat customers had a lower average order value (146.85) than one-time customers (161.49). Order value is right-skewed, with a median of 105.29 versus a mean of 160.58, indicating that a small
# number of high-value orders pull the average upward. São Paulo (SP) generated the most orders with 41,746 orders.
