import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Beauty Booking Assistant",
    page_icon="💄",
    layout="wide"
)

# ---------------- FILE PATHS ----------------
users_path = Path("users.json")
services_path = Path("services.json")
bookings_path = Path("bookings.json")

# ---------------- DEFAULT DATA ----------------
default_users = [
    {
        "id": "1",
        "email": "admin@glamstudio.com",
        "full_name": "Salon Owner",
        "password": "admin123",
        "role": "Admin",
        "registered_at": "2026-03-31 10:00:00"
    }
]

default_services = [
    {
        "service_id": "1",
        "service_name": "Silk Press",
        "price": 65,
        "duration": "1 hour",
        "available_slots": ["2026-04-02 10:00 AM", "2026-04-02 1:00 PM"]
    },
    {
        "service_id": "2",
        "service_name": "Soft Glam Makeup",
        "price": 85,
        "duration": "1.5 hours",
        "available_slots": ["2026-04-03 11:00 AM", "2026-04-03 3:00 PM"]
    }
]

default_bookings = []

# ---------------- LOAD JSON ----------------
if users_path.exists():
    with users_path.open("r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = default_users
    with users_path.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

if services_path.exists():
    with services_path.open("r", encoding="utf-8") as f:
        services = json.load(f)
else:
    services = default_services
    with services_path.open("w", encoding="utf-8") as f:
        json.dump(services, f, indent=4)

if bookings_path.exists():
    with bookings_path.open("r", encoding="utf-8") as f:
        bookings = json.load(f)
else:
    bookings = default_bookings
    with bookings_path.open("w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=4)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------- TITLE ----------------
st.title("💄 AI-Powered Styling & Booking Assistant")

# ---------------- SIDEBAR ----------------
if not st.session_state.logged_in:
    page = st.sidebar.radio("Navigation", ["Register", "Login"])
else:
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "AI Consultation", "Logout"]
    )

# ---------------- REGISTER ----------------
if not st.session_state.logged_in and page == "Register":
    st.subheader("Create Account")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### New User Registration")
            email = st.text_input("Email Address")
            full_name = st.text_input("First and Last Name")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["Client", "Admin"])

            if st.button("Create Account"):
                if not email or not full_name or not password:
                    st.error("Please fill in all fields.")
                else:
                    email_exists = False
                    for user in users:
                        if user["email"] == email:
                            email_exists = True
                            break

                    if email_exists:
                        st.error("An account with that email already exists.")
                    else:
                        with st.spinner("Creating your account..."):
                            time.sleep(2)

                            new_user = {
                                "id": str(len(users) + 1),
                                "email": email,
                                "full_name": full_name,
                                "password": password,
                                "role": role,
                                "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }

                            users.append(new_user)

                            with users_path.open("w", encoding="utf-8") as f:
                                json.dump(users, f, indent=4)

                        st.success("Account created successfully!")

    with col2:
        with st.expander("View User Database"):
            st.dataframe(users)

# ---------------- LOGIN ----------------
elif not st.session_state.logged_in and page == "Login":
    st.subheader("Login")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### User Login")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")

            if st.button("Log In"):
                with st.spinner("Verifying credentials..."):
                    time.sleep(2)

                    found_user = None

                    for user in users:
                        if user["email"] == email and user["password"] == password:
                            found_user = user
                            break

                    if found_user:
                        st.session_state.logged_in = True
                        st.session_state.current_user = found_user
                        st.success(
                            f"Welcome, {found_user['full_name']}! Role: {found_user['role']}"
                        )
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

    with col2:
        st.markdown("### Current User Database")
        st.dataframe(users)

# ---------------- DASHBOARD ----------------
elif st.session_state.logged_in and page == "Dashboard":
    current_user = st.session_state.current_user

    st.subheader(f"Dashboard - {current_user['full_name']}")
    st.write(f"**Role:** {current_user['role']}")

    # ------------ ADMIN DASHBOARD ------------
    if current_user["role"] == "Admin":
        admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(
            ["Manage Services", "Manage Time Slots", "View Bookings", "Data"]
        )

        with admin_tab1:
            st.markdown("### Add New Service")
            service_name = st.text_input("Service Name")
            price = st.number_input("Price", min_value=0, step=5)
            duration = st.selectbox("Duration", ["30 mins", "1 hour", "1.5 hours", "2 hours"])

            if st.button("Add Service"):
                if not service_name or not duration:
                    st.error("Please complete all service fields.")
                else:
                    with st.spinner("Adding service..."):
                        time.sleep(1)

                        new_service = {
                            "service_id": str(len(services) + 1),
                            "service_name": service_name,
                            "price": price,
                            "duration": duration,
                            "available_slots": []
                        }

                        services.append(new_service)

                        with services_path.open("w", encoding="utf-8") as f:
                            json.dump(services, f, indent=4)

                    st.success("Service added successfully!")

            st.markdown("### Current Services")
            st.dataframe(services)

        with admin_tab2:
            st.markdown("### Add Available Time Slot")

            if len(services) > 0:
                service_options = []
                for service in services:
                    service_options.append(
                        f"{service['service_id']} - {service['service_name']}"
                    )

                selected_service = st.selectbox("Choose Service", service_options)
                new_slot = st.text_input("Enter New Time Slot", placeholder="2026-04-05 2:00 PM")

                if st.button("Add Time Slot"):
                    service_id = selected_service.split(" - ")[0]

                    for service in services:
                        if service["service_id"] == service_id:
                            service["available_slots"].append(new_slot)

                    with services_path.open("w", encoding="utf-8") as f:
                        json.dump(services, f, indent=4)

                    st.success("Time slot added successfully!")

            st.markdown("### Services with Slots")
            st.dataframe(services)

        with admin_tab3:
            st.markdown("### Client Bookings")
            st.dataframe(bookings)

        with admin_tab4:
            with st.expander("Users"):
                st.dataframe(users)
            with st.expander("Services"):
                st.dataframe(services)
            with st.expander("Bookings"):
                st.dataframe(bookings)

    # ------------ CLIENT DASHBOARD ------------
    elif current_user["role"] == "Client":
        client_tab1, client_tab2, client_tab3 = st.tabs(
            ["View Services", "Book Appointment", "My Bookings"]
        )

        with client_tab1:
            st.markdown("### Available Beauty Services")
            st.dataframe(services)

        with client_tab2:
            st.markdown("### Book an Appointment")

            if len(services) > 0:
                service_options = []
                for service in services:
                    service_options.append(
                        f"{service['service_id']} - {service['service_name']} (${service['price']})"
                    )

                selected_service = st.selectbox("Choose a Service", service_options)

                selected_service_id = selected_service.split(" - ")[0]

                selected_slots = []
                selected_service_name = ""

                for service in services:
                    if service["service_id"] == selected_service_id:
                        selected_slots = service["available_slots"]
                        selected_service_name = service["service_name"]

                if len(selected_slots) > 0:
                    chosen_slot = st.selectbox("Choose an Available Time Slot", selected_slots)

                    if st.button("Book Appointment"):
                        with st.spinner("Booking your appointment..."):
                            time.sleep(2)

                            new_booking = {
                                "booking_id": str(len(bookings) + 1),
                                "client_name": current_user["full_name"],
                                "client_email": current_user["email"],
                                "service_name": selected_service_name,
                                "appointment_time": chosen_slot,
                                "status": "Booked"
                            }

                            bookings.append(new_booking)

                            for service in services:
                                if service["service_id"] == selected_service_id:
                                    if chosen_slot in service["available_slots"]:
                                        service["available_slots"].remove(chosen_slot)

                            with bookings_path.open("w", encoding="utf-8") as f:
                                json.dump(bookings, f, indent=4)

                            with services_path.open("w", encoding="utf-8") as f:
                                json.dump(services, f, indent=4)

                        st.success("Appointment booked successfully!")
                else:
                    st.error("No available time slots for this service right now.")

        with client_tab3:
            st.markdown("### My Bookings")

            my_bookings = []
            for booking in bookings:
                if booking["client_email"] == current_user["email"]:
                    my_bookings.append(booking)

            st.dataframe(my_bookings)

            if len(my_bookings) > 0:
                cancel_options = []
                for booking in my_bookings:
                    cancel_options.append(
                        f"{booking['booking_id']} - {booking['service_name']} - {booking['appointment_time']}"
                    )

                cancel_choice = st.selectbox("Select Booking to Cancel", cancel_options)

                if st.button("Cancel Booking"):
                    booking_id = cancel_choice.split(" - ")[0]

                    cancelled_booking = None

                    for booking in bookings:
                        if booking["booking_id"] == booking_id:
                            booking["status"] = "Cancelled"
                            cancelled_booking = booking
                            break

                    if cancelled_booking:
                        for service in services:
                            if service["service_name"] == cancelled_booking["service_name"]:
                                service["available_slots"].append(cancelled_booking["appointment_time"])

                        with bookings_path.open("w", encoding="utf-8") as f:
                            json.dump(bookings, f, indent=4)

                        with services_path.open("w", encoding="utf-8") as f:
                            json.dump(services, f, indent=4)

                        st.success("Booking cancelled successfully!")

# ---------------- AI CONSULTATION ----------------
elif st.session_state.logged_in and page == "AI Consultation":
    current_user = st.session_state.current_user

    st.subheader("AI Styling & Booking Assistant")
    st.write("Answer a few questions for a simulated beauty consultation.")

    with st.container(border=True):
        occasion = st.selectbox(
            "What is the occasion?",
            ["Everyday Look", "Birthday", "Wedding", "Photoshoot", "Date Night"]
        )

        style_preference = st.selectbox(
            "What style do you want?",
            ["Natural", "Soft Glam", "Full Glam", "Elegant", "Trendy"]
        )

        hair_goal = st.selectbox(
            "What are you looking for?",
            ["Hair Styling", "Makeup", "Both"]
        )

        concern = st.selectbox(
            "Any main concern?",
            ["None", "Sensitive Skin", "Frizz", "Need Long-Lasting Look", "Beginner-Friendly Style"]
        )

        if st.button("Get AI Recommendation"):
            with st.spinner("Analyzing your beauty preferences..."):
                time.sleep(2)

                recommendation = ""

                if hair_goal == "Hair Styling":
                    if style_preference == "Natural":
                        recommendation = "AI Suggestion: A Silk Press or simple curls would match your desired natural look."
                    elif style_preference == "Elegant":
                        recommendation = "AI Suggestion: A sleek bun or soft waves would be a great elegant style choice."
                    else:
                        recommendation = "AI Suggestion: A styled look with volume and hold would fit your request."

                elif hair_goal == "Makeup":
                    if style_preference == "Soft Glam":
                        recommendation = "AI Suggestion: Soft Glam Makeup would be a strong match for your occasion and style preference."
                    elif style_preference == "Natural":
                        recommendation = "AI Suggestion: A natural beat with light coverage and gloss would work well."
                    else:
                        recommendation = "AI Suggestion: A full makeup appointment may best match the look you want."

                elif hair_goal == "Both":
                    recommendation = "AI Suggestion: Booking both a hair styling service and makeup service would best support your overall beauty goal."

                st.success(recommendation)

                if concern == "Sensitive Skin":
                    st.info("Consultation Note: You may want to request hypoallergenic or skin-friendly products.")
                elif concern == "Frizz":
                    st.info("Consultation Note: Ask your stylist about anti-frizz products and humidity-resistant styling.")
                elif concern == "Need Long-Lasting Look":
                    st.info("Consultation Note: A setting spray, finishing powder, or long-wear styling option may help.")

# ---------------- LOGOUT ----------------
elif st.session_state.logged_in and page == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("You have been logged out.")
    st.rerun()