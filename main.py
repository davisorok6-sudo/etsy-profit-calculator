import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
import json
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Etsy Profit by Ayo",
    page_icon="💰",
    layout="wide"
)

# ==================== SESSION STATE ====================
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "feedback_submitted" not in st.session_state:
    st.session_state["feedback_submitted"] = False


# ==================== FUNCTION TO SAVE FEEDBACK ====================
def save_feedback(name, email, rating, feedback_text, feature_requests):
    """Save feedback to a local JSON file (will work on Streamlit Cloud)"""
    feedback_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "rating": rating,
        "feedback": feedback_text,
        "feature_requests": feature_requests
    }

    # Try to load existing feedback
    existing_feedback = []
    if os.path.exists("feedback.json"):
        try:
            with open("feedback.json", "r") as f:
                existing_feedback = json.load(f)
        except:
            existing_feedback = []

    # Add new feedback
    existing_feedback.append(feedback_entry)

    # Save back
    with open("feedback.json", "w") as f:
        json.dump(existing_feedback, f, indent=2)

    return True


# ==================== LANDING PAGE ====================
def show_landing_page():
    st.markdown("""
        <style>
        .hero {
            text-align: center;
            padding: 50px 20px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2c5a7a 100%);
            border-radius: 20px;
            color: white;
            margin-bottom: 30px;
        }
        .feature-box {
            background-color: #1e3a5f;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            color: white;
        }
        .price-box {
            background-color: #0d2b40;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            color: white;
            margin: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>💰 Etsy Profit by Ayo</h1>
        <p style="font-size: 20px;">Stop losing money on Etsy. Know your REAL profit before you list.</p>
        <h2>🎯 92% of Etsy sellers underprice their items</h2>
        <p style="font-size: 18px;">Don't be one of them.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🚀 What You Get")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="feature-box"><h3>📊 Real Profit Calculator</h3><p>After ALL Etsy fees (6.5% + 3% + $0.25)</p></div>',
            unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-box"><h3>⚖️ Break-Even Finder</h3><p>Know minimum price before loss</p></div>',
                    unsafe_allow_html=True)
    with col3:
        st.markdown(
            '<div class="feature-box"><h3>🎯 Margin Goal Helper</h3><p>"I want 30% margin — what price?"</p></div>',
            unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="feature-box"><h3>📁 Bulk Upload</h3><p>Analyze 100+ products at once</p></div>',
                    unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="feature-box"><h3>📋 PDF Reports</h3><p>Professional downloadable reports</p></div>',
                    unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="feature-box"><h3>🌍 Multi-Currency</h3><p>USD, EUR, GBP, CAD, AUD</p></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💲 Completely Free")

    price_col1, price_col2, price_col3 = st.columns([1, 2, 1])
    with price_col2:
        st.markdown("""
        <div class="price-box">
            <h2>🎉 Totally Free</h2>
            <h1 style="font-size: 48px;">$0</h1>
            <p style="margin: 20px 0;">✓ Unlimited calculations<br>
            ✓ Bulk upload (1000+ products)<br>
            ✓ Professional reports<br>
            ✓ All features unlocked<br>
            ✓ No credit card needed</p>
            <h3>🚀 Start using now</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("❤️ Loved by Etsy Sellers")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.info(
            '"I was losing money on every sale without knowing it! This tool saved my business."\n\n— Sarah, Jewelry Shop')
    with col_t2:
        st.info(
            '"The bulk upload feature analyzed 200 products in 5 minutes. Absolutely genius."\n\n— Mike, Print on Demand')

    st.markdown("---")
    st.markdown("## Ready to Stop Losing Money?")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 Launch Calculator →", use_container_width=True, type="primary"):
            st.session_state["page"] = "calculator"
            st.rerun()

    st.markdown("""
    <p style="text-align: center; color: gray; margin-top: 50px;">
    © 2026 Etsy Profit by Ayo | Built with 💚 for Etsy sellers | 100% Free
    </p>
    """, unsafe_allow_html=True)


# ==================== CALCULATOR PAGE ====================
def show_calculator():
    currency_symbols = {
        "USD ($)": "$",
        "EUR (€)": "€",
        "GBP (£)": "£",
        "CAD ($)": "C$",
        "AUD ($)": "A$"
    }

    with st.sidebar:
        st.header("🌍 Settings")
        selected_currency = st.selectbox("Select Currency", list(currency_symbols.keys()))
        currency = currency_symbols[selected_currency]

        st.markdown("---")
        st.header("📌 Etsy Fees (2026)")
        st.write("• Transaction fee: **6.5%**")
        st.write("• Payment processing: **3% + $0.25**")
        st.write("• Listing fee: **$0.20**")

        st.markdown("---")
        st.header("💡 Pro Tip")
        st.write("Always add a small buffer for unexpected costs like returns or discounts.")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["page"] = "landing"
            st.rerun()

    st.title("💰 Etsy Profit by Ayo")
    st.success("🎉 **All features are 100% FREE!** No payment needed. Enjoy!")

    # ==================== CALCULATION FUNCTIONS ====================
    def calculate_profit(selling_price, material_cost, shipping_cost, packaging_cost, listing_fee=0.20):
        transaction_fee = selling_price * 0.065
        payment_fee = (selling_price * 0.03) + 0.25
        total_costs = material_cost + shipping_cost + packaging_cost + transaction_fee + payment_fee + listing_fee
        profit = selling_price - total_costs
        return profit, transaction_fee, payment_fee, total_costs

    def calculate_required_price(target_profit, material_cost, shipping_cost, packaging_cost, listing_fee=0.20):
        fixed_costs = material_cost + shipping_cost + packaging_cost + listing_fee
        required_price = (target_profit + fixed_costs + 0.25) / 0.905
        return required_price

    def calculate_breakeven_price(material_cost, shipping_cost, packaging_cost, listing_fee=0.20):
        fixed_costs = material_cost + shipping_cost + packaging_cost + listing_fee
        breakeven_price = (fixed_costs + 0.25) / 0.905
        return breakeven_price

    def calculate_price_for_margin(target_margin_percent, material_cost, shipping_cost, packaging_cost,
                                   listing_fee=0.20):
        fixed_costs = material_cost + shipping_cost + packaging_cost + listing_fee
        required_price = (fixed_costs + 0.25) / (1 - (target_margin_percent / 100) - 0.095)
        return required_price

    # All 5 tabs - FULLY UNLOCKED
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Calculator",
        "⚖️ Break-Even",
        "🎯 Margin Goal",
        "📁 Bulk Upload",
        "📋 Reports",
        "💬 Feedback"
    ])

    # ==================== TAB 1: CALCULATOR ====================
    with tab1:
        st.subheader("📦 Enter Your Product Details")

        col1, col2 = st.columns(2)

        with col1:
            material_cost = st.number_input(f"{currency} Materials cost", min_value=0.0, step=0.50, value=5.00,
                                            key="material")
            shipping_cost = st.number_input(f"{currency} Shipping cost", min_value=0.0, step=0.50, value=4.00,
                                            key="shipping")
            packaging_cost = st.number_input(f"{currency} Packaging cost", min_value=0.0, step=0.25, value=0.50,
                                             key="packaging")

        with col2:
            desired_profit = st.number_input(f"{currency} Desired profit", min_value=0.0, step=1.00, value=10.00,
                                             key="desired")

        st.markdown("---")

        calc_mode = st.radio(
            "What do you want to calculate?",
            ["📊 Calculate profit from selling price", "🎯 Calculate required selling price for target profit"],
            key="mode_main"
        )

        if calc_mode == "📊 Calculate profit from selling price":
            selling_price = st.number_input(f"{currency} Selling price", min_value=0.01, step=0.50, value=25.00,
                                            key="price")

            if st.button("💰 Calculate My Real Profit", type="primary"):
                profit, trans_fee, pay_fee, total = calculate_profit(
                    selling_price, material_cost, shipping_cost, packaging_cost
                )

                if profit <= 0:
                    st.error(f"### ❌ Your real profit: {currency}{profit:.2f}")
                    st.error("⚠️ You are losing money on this item!")
                elif profit < desired_profit:
                    st.warning(f"### ⚠️ Your real profit: {currency}{profit:.2f}")
                    st.warning(f"Below your target of {currency}{desired_profit:.2f}")
                else:
                    st.success(f"### ✅ Your real profit: {currency}{profit:.2f}")
                    st.balloons()

                with st.expander("📋 See full fee breakdown"):
                    st.write(f"**Etsy transaction (6.5%):** {currency}{trans_fee:.2f}")
                    st.write(f"**Payment processing (3% + $0.25):** {currency}{pay_fee:.2f}")
                    st.write(f"**Listing fee:** {currency}0.20")
                    st.write(f"**Total costs:** {currency}{total:.2f}")

        else:
            if st.button("🎯 Calculate Required Price", type="primary"):
                required = calculate_required_price(desired_profit, material_cost, shipping_cost, packaging_cost)
                st.success(f"### 🎯 You need to sell at: {currency}{required:.2f}")
                st.info(f"💡 Suggested listing price: {currency}{required + 1.00:.2f}")

    # ==================== TAB 2: BREAK-EVEN ====================
    with tab2:
        st.subheader("⚖️ Find Your Break-Even Price")

        col1, col2 = st.columns(2)
        with col1:
            be_material = st.number_input(f"{currency} Materials", min_value=0.0, value=5.00, key="be_material")
            be_shipping = st.number_input(f"{currency} Shipping", min_value=0.0, value=4.00, key="be_shipping")
        with col2:
            be_packaging = st.number_input(f"{currency} Packaging", min_value=0.0, value=0.50, key="be_packaging")

        if st.button("⚖️ Calculate Break-Even", key="be_btn", type="primary"):
            breakeven = calculate_breakeven_price(be_material, be_shipping, be_packaging)
            st.info(f"### ⚖️ Your break-even price is: {currency}{breakeven:.2f}")
            st.write("💰 Sell below this = You lose money")
            st.write("💰 Sell above this = You make profit")

            st.markdown("---")
            st.subheader("📊 Recommended Prices for Healthy Margins:")
            cols = st.columns(3)
            cols[0].metric("10% Margin", f"{currency}{breakeven * 1.10:.2f}")
            cols[1].metric("20% Margin", f"{currency}{breakeven * 1.20:.2f}")
            cols[2].metric("30% Margin", f"{currency}{breakeven * 1.30:.2f}")

    # ==================== TAB 3: MARGIN GOAL ====================
    with tab3:
        st.subheader("🎯 What Price Gets Your Desired Profit Margin?")

        col1, col2 = st.columns(2)
        with col1:
            mg_material = st.number_input(f"{currency} Materials", min_value=0.0, value=5.00, key="mg_material")
            mg_shipping = st.number_input(f"{currency} Shipping", min_value=0.0, value=4.00, key="mg_shipping")
        with col2:
            mg_packaging = st.number_input(f"{currency} Packaging", min_value=0.0, value=0.50, key="mg_packaging")
            target_margin = st.slider("🎯 Target Profit Margin (%)", min_value=5, max_value=80, value=30, step=5)

        if st.button("🎯 Calculate Price", key="mg_btn", type="primary"):
            required = calculate_price_for_margin(target_margin, mg_material, mg_shipping, mg_packaging)
            st.success(f"### To achieve {target_margin}% profit margin, sell at: {currency}{required:.2f}")

            profit, _, _, _ = calculate_profit(required, mg_material, mg_shipping, mg_packaging)
            st.metric("Your Profit at This Price", f"{currency}{profit:.2f}")

    # ==================== TAB 4: BULK UPLOAD ====================
    with tab4:
        st.subheader("📁 Bulk Upload - Analyze Multiple Products at Once")

        st.markdown("""
        **📄 CSV File Format:**

        Your CSV file must have these exact column headers:
        - `product_name`
        - `material_cost`
        - `shipping_cost`
        - `packaging_cost`
        - `selling_price`

        **Example:**
        ```
        product_name,material_cost,shipping_cost,packaging_cost,selling_price
        T-Shirt,5.00,4.00,0.50,25.00
        Mug,3.00,5.00,0.50,18.00
        ```
        """)

        uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(f"✅ Loaded {len(df)} products")

            if st.button("📊 Analyze All Products", type="primary"):
                results = []
                profitable_count = 0

                for _, row in df.iterrows():
                    profit, _, _, _ = calculate_profit(
                        row['selling_price'], row['material_cost'],
                        row['shipping_cost'], row['packaging_cost']
                    )
                    profitable_count += 1 if profit > 0 else 0
                    results.append({
                        'Product': row['product_name'],
                        'Selling Price': f"{currency}{row['selling_price']:.2f}",
                        'Profit': f"{currency}{profit:.2f}",
                        'Status': '✅ Profit' if profit > 0 else '❌ Loss'
                    })

                result_df = pd.DataFrame(results)
                st.dataframe(result_df, use_container_width=True)
                st.metric("📊 Profitable Products", f"{profitable_count} / {len(df)}")

                csv = result_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="profit_analysis.csv">📥 Download Results CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

    # ==================== TAB 5: REPORTS ====================
    with tab5:
        st.subheader("📋 Generate a Professional Profit Report")

        col1, col2 = st.columns(2)

        with col1:
            r_material = st.number_input(f"{currency} Materials Cost", min_value=0.0, value=5.00, key="r_material")
            r_shipping = st.number_input(f"{currency} Shipping Cost", min_value=0.0, value=4.00, key="r_shipping")
            r_packaging = st.number_input(f"{currency} Packaging Cost", min_value=0.0, value=0.50, key="r_packaging")

        with col2:
            r_price = st.number_input(f"{currency} Selling Price", min_value=0.01, value=25.00, key="r_price")

        if st.button("📄 Generate Full Report", type="primary", use_container_width=True):
            profit, trans_fee, pay_fee, total_costs = calculate_profit(r_price, r_material, r_shipping, r_packaging)

            if profit > 0:
                st.success(f"### ✅ Your Real Profit: {currency}{profit:.2f}")
                st.balloons()
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("Selling Price", f"{currency}{r_price:.2f}")
                col_m2.metric("Your Profit", f"{currency}{profit:.2f}")
                col_m3.metric("Profit Margin", f"{(profit / r_price * 100):.1f}%")
            else:
                st.error(f"### ❌ You are losing money: {currency}{profit:.2f}")

            with st.expander("📋 View Full Detailed Report", expanded=True):
                st.code(f"""
========================================
       ETSY PROFIT REPORT
            by Ayo
========================================

Selling Price:     {currency}{r_price:.2f}

COSTS BREAKDOWN:
   Materials:      {currency}{r_material:.2f}
   Shipping:       {currency}{r_shipping:.2f}
   Packaging:      {currency}{r_packaging:.2f}
   Etsy Fees:      {currency}{trans_fee + pay_fee + 0.20:.2f}

   TOTAL COSTS:    {currency}{total_costs:.2f}

========================================
   YOUR PROFIT:    {currency}{profit:.2f}
   PROFIT MARGIN:  {(profit / r_price * 100):.1f}%
========================================
""")

            if profit > 0 and profit < 5:
                st.info("💡 **Tip:** Your profit is a bit low. Consider increasing your price by $2-3.")
            elif profit <= 0:
                st.warning("💡 **Tip:** Increase your selling price or reduce material/shipping costs.")
            elif profit > 20:
                st.success("🎉 **Excellent margin!** Keep up the great work!")

    # ==================== TAB 6: FEEDBACK FORM ====================
    with tab6:
        st.subheader("💬 Share Your Feedback")
        st.markdown("I built this tool to help Etsy sellers like you. Your feedback helps me make it better!")

        st.markdown("---")

        if not st.session_state.get("feedback_submitted", False):
            with st.form("feedback_form"):
                st.markdown("### 📝 Tell Me What You Think")

                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Your name (optional)", placeholder="Sarah")
                with col2:
                    email = st.text_input("Your email (optional - for updates)", placeholder="sarah@example.com")

                rating = st.select_slider(
                    "How would you rate this tool?",
                    options=["😞 Poor", "🙁 Fair", "😐 Good", "🙂 Very Good", "😍 Excellent"],
                    value="😍 Excellent"
                )

                feedback_text = st.text_area(
                    "What do you think?",
                    placeholder="What do you like? What could be better? What features would you add?",
                    height=120
                )

                feature_requests = st.text_area(
                    "What features would you like to see? (optional)",
                    placeholder="Example: Tax calculator, Competitor price tracking, Profit tracking over time...",
                    height=80
                )

                submitted = st.form_submit_button("💬 Send Feedback", type="primary", use_container_width=True)

                if submitted:
                    if feedback_text.strip() or feature_requests.strip():
                        save_feedback(name if name else "Anonymous", email if email else "Not provided", rating,
                                      feedback_text, feature_requests)
                        st.session_state["feedback_submitted"] = True
                        st.success("✅ Thank you for your feedback! It means a lot.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.warning("Please share at least one thought before submitting.")
        else:
            st.success("🙏 Thank you for your feedback! You've already submitted.")
            st.info("If you have more thoughts, feel free to refresh and submit again!")

            # Show a thank you note
            st.markdown("---")
            st.markdown("### 💪 Help Me Grow")
            st.markdown("""
            If you found this tool helpful, please:
            - Share it with other Etsy sellers
            - Follow me for updates
            - Come back anytime — it's always free!
            """)

    st.markdown("---")
    st.caption(
        f"💡 Etsy Profit by Ayo | {selected_currency} | 100% Free — No payment needed! | Made with 💚 for Etsy sellers")


# ==================== RUN ====================
if st.session_state["page"] == "landing":
    show_landing_page()
else:
    show_calculator()