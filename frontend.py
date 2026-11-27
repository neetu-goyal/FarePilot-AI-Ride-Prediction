
import streamlit as st
import requests
import folium
import pandas as pd
import streamlit.components.v1 as components


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Global Ride Booking System",
    page_icon="🚕",
    layout="wide"
)

st.title("🌍 Global Ride Booking & Fare Estimation")
st.write(
    "Select your country, locations and vehicle "
    "to calculate your estimated ride fare."
)


# =====================================================
# 2. COUNTRY AND CURRENCY CONFIGURATION
# =====================================================

COUNTRIES = {
    "India": {
        "code": "in",
        "currency": "INR",
        "symbol": "₹",
        "currency_name": "Indian Rupee"
    },

    "United States": {
        "code": "us",
        "currency": "USD",
        "symbol": "$",
        "currency_name": "US Dollar"
    },

    "United Kingdom": {
        "code": "gb",
        "currency": "GBP",
        "symbol": "£",
        "currency_name": "British Pound"
    }
}


# =====================================================
# 3. COUNTRY-WISE VEHICLE RATE CARD
# =====================================================

# These are configurable DEMO rates.
# Replace them with verified local rates before
# presenting them as real-world prices.

RATE_CARD = {

    "India": {

        "Bike": {
            "base": 20,
            "per_km": 8,
            "per_min": 0,
            "minimum": 40,
            "max_passengers": 1
        },

        "Auto": {
            "base": 39,
            "per_km": 10,
            "per_min": 0,
            "minimum": 60,
            "max_passengers": 3
        },

        "Mini Car": {
            "base": 49,
            "per_km": 13,
            "per_min": 0,
            "minimum": 80,
            "max_passengers": 4
        },

        "Sedan": {
            "base": 50,
            "per_km": 17,
            "per_min": 0,
            "minimum": 100,
            "max_passengers": 4
        },

        "SUV": {
            "base": 60,
            "per_km": 20,
            "per_min": 0,
            "minimum": 120,
            "max_passengers": 6
        }
    },


    "United States": {

        "Bike": {
            "base": 2.50,
            "per_km": 1.50,
            "per_min": 0,
            "minimum": 5,
            "max_passengers": 1
        },

        "Auto": {
            "base": 3.50,
            "per_km": 2.00,
            "per_min": 0,
            "minimum": 7,
            "max_passengers": 3
        },

        "Mini Car": {
            "base": 4.00,
            "per_km": 2.20,
            "per_min": 0,
            "minimum": 8,
            "max_passengers": 4
        },

        "Sedan": {
            "base": 5.00,
            "per_km": 2.80,
            "per_min": 0,
            "minimum": 10,
            "max_passengers": 4
        },

        "SUV": {
            "base": 6.00,
            "per_km": 3.50,
            "per_min": 0,
            "minimum": 12,
            "max_passengers": 6
        }
    },


    "United Kingdom": {

        "Bike": {
            "base": 2.00,
            "per_km": 1.20,
            "per_min": 0,
            "minimum": 4,
            "max_passengers": 1
        },

        "Auto": {
            "base": 3.00,
            "per_km": 1.60,
            "per_min": 0,
            "minimum": 6,
            "max_passengers": 3
        },

        "Mini Car": {
            "base": 3.50,
            "per_km": 1.80,
            "per_min": 0,
            "minimum": 7,
            "max_passengers": 4
        },

        "Sedan": {
            "base": 4.00,
            "per_km": 2.20,
            "per_min": 0,
            "minimum": 8,
            "max_passengers": 4
        },

        "SUV": {
            "base": 5.00,
            "per_km": 2.80,
            "per_min": 0,
            "minimum": 10,
            "max_passengers": 6
        }
    }
}


# =====================================================
# 4. LIVE CURRENCY EXCHANGE RATE
# =====================================================

@st.cache_data(ttl=3600)
def get_exchange_rates():

    url = "https://open.er-api.com/v6/latest/INR"

    try:

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("result") == "success":
            return data["rates"]

        return None

    except requests.RequestException:
        return None


def convert_to_inr(amount, currency, rates):

    if currency == "INR":
        return amount

    if not rates:
        return None

    currency_rate = rates.get(currency)

    if not currency_rate:
        return None

    return amount / currency_rate


# =====================================================
# 5. LOCATION SEARCH / GEOCODING
# =====================================================

def get_coordinates(location, country_code, country_name):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{location}, {country_name}",
        "format": "json",
        "limit": 1,
        "countrycodes": country_code
    }

    headers = {
        "User-Agent": "GlobalRideFareProject/1.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        results = response.json()

        if results:

            lat = float(results[0]["lat"])
            lon = float(results[0]["lon"])

            return lat, lon

        return None

    except requests.RequestException:
        return None


# =====================================================
# 6. ROAD ROUTE / DISTANCE / DURATION
# =====================================================

def get_route(pickup_coords, drop_coords):

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{pickup_coords[1]},{pickup_coords[0]};"
        f"{drop_coords[1]},{drop_coords[0]}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if data["code"] == "Ok" and data["routes"]:

            route = data["routes"][0]

            distance_km = route["distance"] / 1000

            duration_minutes = route["duration"] / 60

            coordinates = route["geometry"]["coordinates"]

            route_points = [
                (lat, lon)
                for lon, lat in coordinates
            ]

            return (
                distance_km,
                duration_minutes,
                route_points
            )

        return None

    except requests.RequestException:
        return None


# =====================================================
# 7. FARE CALCULATION
# =====================================================

def calculate_fare(country, vehicle, distance, duration):

    rate = RATE_CARD[country][vehicle]

    base_fare = rate["base"]

    distance_charge = distance * rate["per_km"]

    time_charge = duration * rate["per_min"]

    subtotal = (
        base_fare
        + distance_charge
        + time_charge
    )

    minimum_adjustment = max(
        0,
        rate["minimum"] - subtotal
    )

    total_fare = max(
        subtotal,
        rate["minimum"]
    )

    return {

        "Base Fare": round(base_fare, 2),

        "Distance Charge": round(
            distance_charge, 2
        ),

        "Time Charge": round(
            time_charge, 2
        ),

        "Minimum Fare Adjustment": round(
            minimum_adjustment, 2
        ),

        "Total Fare": round(
            total_fare, 2
        )
    }


# =====================================================
# 8. COUNTRY SELECTION
# =====================================================

st.subheader("🌍 Select Country")

country = st.selectbox(
    "Choose your country",
    list(COUNTRIES.keys())
)

country_info = COUNTRIES[country]

currency = country_info["currency"]

symbol = country_info["symbol"]

st.info(
    f"Selected Country: {country} | "
    f"Currency: {currency} ({symbol}) | "
    f"Currency Name: {country_info['currency_name']}"
)


# =====================================================
# 9. PICKUP AND DROP LOCATION
# =====================================================

st.subheader("📍 Select Pickup and Drop Locations")

col1, col2 = st.columns(2)

with col1:

    pickup = st.text_input(
        "Pickup Location",
        placeholder="Enter pickup location"
    )

with col2:

    drop = st.text_input(
        "Drop Location",
        placeholder="Enter drop location"
    )


# =====================================================
# 10. VEHICLE SELECTION
# =====================================================

st.subheader("🚘 Select Vehicle Type")

vehicle = st.selectbox(
    "Choose your vehicle",
    list(RATE_CARD[country].keys())
)

vehicle_info = RATE_CARD[country][vehicle]

max_passengers = vehicle_info["max_passengers"]

passengers = st.selectbox(
    "Number of Passengers",
    list(range(1, max_passengers + 1))
)

payment_method = st.selectbox(
    "Payment Method",
    ["Cash", "UPI", "Card"]
)


# =====================================================
# 11. SHOW SELECTED VEHICLE RATE
# =====================================================

st.write("### Selected Vehicle Pricing")

rate_col1, rate_col2, rate_col3 = st.columns(3)

rate_col1.metric(
    "Base Fare",
    f"{symbol}{vehicle_info['base']:.2f}"
)

rate_col2.metric(
    "Per KM Rate",
    f"{symbol}{vehicle_info['per_km']:.2f}"
)

rate_col3.metric(
    "Minimum Fare",
    f"{symbol}{vehicle_info['minimum']:.2f}"
)


# =====================================================
# 12. VIEW ALL COUNTRY VEHICLE RATES
# =====================================================

with st.expander("View Complete Vehicle Rate Card"):

    rate_rows = []

    for vehicle_name, rate in RATE_CARD[country].items():

        rate_rows.append({

            "Vehicle": vehicle_name,

            "Base Fare": f"{symbol}{rate['base']:.2f}",

            "Per KM": f"{symbol}{rate['per_km']:.2f}",

            "Per Minute": f"{symbol}{rate['per_min']:.2f}",

            "Minimum Fare": f"{symbol}{rate['minimum']:.2f}",

            "Passengers": rate["max_passengers"]
        })

    st.dataframe(
        pd.DataFrame(rate_rows),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 13. CALCULATE RIDE BUTTON
# =====================================================

if st.button("Calculate Ride Fare", type="primary"):

    if not pickup.strip() or not drop.strip():

        st.error("Please enter both pickup and drop locations.")

    else:

        with st.spinner("Searching locations and calculating route..."):

            country_code = country_info["code"]

            pickup_coords = get_coordinates(
                pickup,
                country_code,
                country
            )

            drop_coords = get_coordinates(
                drop,
                country_code,
                country
            )

            if pickup_coords is None:

                st.error(
                    "Pickup location not found. "
                    "Please check the spelling or enter a nearby landmark."
                )

            elif drop_coords is None:

                st.error(
                    "Drop location not found. "
                    "Please check the spelling or enter a nearby landmark."
                )

            else:

                route_data = get_route(
                    pickup_coords,
                    drop_coords
                )

                if route_data is None:

                    st.error(
                        "Road route not available. "
                        "Please try different locations."
                    )

                else:

                    distance, duration, route_points = route_data

                    fare = calculate_fare(
                        country,
                        vehicle,
                        distance,
                        duration
                    )

                    total_fare = fare["Total Fare"]

                    # =================================
                    # CURRENCY CONVERSION
                    # =================================

                    exchange_rates = get_exchange_rates()

                    inr_fare = convert_to_inr(
                        total_fare,
                        currency,
                        exchange_rates
                    )

                    # =================================
                    # RIDE SUMMARY
                    # =================================

                    st.success("Ride calculated successfully!")

                    st.subheader("📊 Ride Summary")

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Road Distance",
                        f"{distance:.2f} KM"
                    )

                    c2.metric(
                        "Estimated Duration",
                        f"{duration:.0f} Minutes"
                    )

                    c3.metric(
                        "Total Fare",
                        f"{symbol}{total_fare:.2f}"
                    )

                    if inr_fare is not None:

                        st.metric(
                            "Approximate INR Equivalent",
                            f"₹{inr_fare:,.2f}"
                        )

                    else:

                        st.warning(
                            "Live currency conversion is unavailable. "
                            "Local currency fare is still available."
                        )

                    # =================================
                    # MAP
                    # =================================

                    st.subheader("🗺️ Ride Route Map")

                    center_lat = (
                        pickup_coords[0] + drop_coords[0]
                    ) / 2

                    center_lon = (
                        pickup_coords[1] + drop_coords[1]
                    ) / 2

                    ride_map = folium.Map(
                        location=[center_lat, center_lon],
                        zoom_start=12
                    )

                    folium.Marker(
                        pickup_coords,
                        popup=f"Pickup: {pickup}",
                        tooltip="Pickup Location",
                        icon=folium.Icon(
                            color="green",
                            icon="play"
                        )
                    ).add_to(ride_map)

                    folium.Marker(
                        drop_coords,
                        popup=f"Drop: {drop}",
                        tooltip="Drop Location",
                        icon=folium.Icon(
                            color="red",
                            icon="stop"
                        )
                    ).add_to(ride_map)

                    folium.PolyLine(
                        route_points,
                        color="blue",
                        weight=5,
                        opacity=0.8
                    ).add_to(ride_map)

                    ride_map.fit_bounds(
                        [pickup_coords, drop_coords]
                    )

                    components.html(
                        ride_map.get_root().render(),
                        height=500
                    )

                    # =================================
                    # FARE BREAKDOWN
                    # =================================

                    st.subheader("🧾 Fare Breakdown")

                    fare_rows = []

                    for name, amount in fare.items():

                        fare_rows.append({

                            "Description": name,

                            "Amount": f"{symbol}{amount:.2f}"
                        })

                    st.dataframe(
                        pd.DataFrame(fare_rows),
                        use_container_width=True,
                        hide_index=True
                    )

                    # =================================
                    # BOOKING DETAILS
                    # =================================

                    st.subheader("📋 Booking Details")

                    booking_details = {

                        "Country": country,

                        "Currency": currency,

                        "Pickup Location": pickup,

                        "Drop Location": drop,

                        "Vehicle": vehicle,

                        "Passengers": passengers,

                        "Payment Method": payment_method,

                        "Distance KM": round(distance, 2),

                        "Duration Minutes": round(duration, 2),

                        "Base Fare": fare["Base Fare"],

                        "Distance Charge": fare["Distance Charge"],

                        "Time Charge": fare["Time Charge"],

                        "Minimum Fare Adjustment": fare["Minimum Fare Adjustment"],

                        "Total Fare": total_fare
                    }

                    if inr_fare is not None:

                        booking_details["Approx INR Equivalent"] = round(
                            inr_fare, 2
                        )

                    for key, value in booking_details.items():

                        st.write(f"**{key}:** {value}")

                    # =================================
                    # DOWNLOAD INVOICE
                    # =================================

                    invoice = pd.DataFrame(
                        list(booking_details.items()),
                        columns=["Details", "Value"]
                    )

                    csv_data = invoice.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="📥 Download Ride Invoice",
                        data=csv_data,
                        file_name="ride_booking_invoice.csv",
                        mime="text/csv"
                    )


# =====================================================
# 14. FOOTER
# =====================================================

st.divider()

st.caption(
    "Global Ride Booking System | "
    "Demo fare rates | "
    "Road route powered by OpenStreetMap and OSRM"
)
