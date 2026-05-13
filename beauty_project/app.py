import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime, date

# ---------------- PAGE CONFIG ----------------
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
    },
    {
        "id": "2",
        "email": "client@gmail.com",
        "full_name": "Client User",
        "password": "client123",
        "role": "Client",
        "registered_at": "2026-03-31 10:00:00"
    }
]

default_services = [
    {
        "service_id": "1",
        "service_name": "Silk Press",
        "price": 65,
        "duration": "1 hour",
        "available_slots": []
    },
    {
        "service_id": "2",
        "service_name": "Soft Glam Makeup",
        "price": 85,
        "duration": "1.5 hours",
        "available_slots": []
    },
    {
        "service_id": "3",
        "service_name": "Full Glam Makeup",
        "price": 120,
        "duration": "2 hours",
        "available_slots": []
    }
]

default_bookings = []

# ---------------- LOAD DATA ----------------
def load_json(path, default_data):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with path.open("w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        return default_data

users = load_json(users_path, default_users)
services = load_json(services_path, default_services)
bookings = load_json(bookings_path, default_bookings)

# ---------------- SAVE FUNCTIONS ----------------
def save_users():
    with users_path.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def save_services():
    with services_path.open("w", encoding="utf-8") as f:
        json.dump(services, f, indent=4)

def save_bookings():
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
    page = st.sidebar.radio("Navigation", ["Dashboard", "AI Consultation", "Logout"])

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
                        new_user = {
                            "id": str(len(users) + 1),
                            "email": email,
                            "full_name": full_name,
                            "password": password,
                            "role": role,
                            "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        users.append(new_user)
                        save_users()

                        st.success("Account created successfully!")

    with col2:
        st.markdown("### User Database")
        st.dataframe(users)

# ---------------- LOGIN ----------------
elif not st.session_state.logged_in and page == "Login":
    st.subheader("Login")

    st.info(
        """
        **Test Accounts**

        Admin: admin@glamstudio.com | Password: admin123  
        Client: client@gmail.com | Password: client123
        """
    )

    with st.container(border=True):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            with st.spinner("Verifying credentials..."):
                time.sleep(1)

                found_user = None

                for user in users:
                    if user["email"] == email and user["password"] == password:
                        found_user = user
                        break

                if found_user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = found_user
                    st.success(f"Welcome, {found_user['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    st.subheader("Current User Database")
    st.dataframe(users)

# ---------------- DASHBOARD ----------------
elif st.session_state.logged_in and page == "Dashboard":
    current_user = st.session_state.current_user

    st.subheader(f"Dashboard - {current_user['full_name']}")
    st.write(f"**Role:** {current_user['role']}")

    # ------------ ADMIN DASHBOARD ------------
    if current_user["role"] == "Admin":
        admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5 = st.tabs(
            [
                "Manage Services",
                "Manage Time Slots",
                "View Bookings",
                "Revenue Dashboard",
                "Search Bookings"
            ]
        )

        # -------- MANAGE SERVICES --------
        with admin_tab1:
            st.markdown("### Add New Service")

            service_name = st.text_input("Service Name")
            price = st.number_input("Price", min_value=0, step=5)
            duration = st.selectbox(
                "Duration",
                ["30 mins", "1 hour", "1.5 hours", "2 hours"]
            )

            if st.button("Add Service"):
                if service_name.strip() == "":
                    st.error("Please enter a service name.")
                else:
                    new_service = {
                        "service_id": str(len(services) + 1),
                        "service_name": service_name,
                        "price": price,
                        "duration": duration,
                        "available_slots": []
                    }

                    services.append(new_service)
                    save_services()
                    st.success("Service added successfully!")
                    st.rerun()

            st.markdown("### Current Services")
            st.dataframe(services)

            st.divider()
            st.markdown("### Update Service")

            if len(services) > 0:
                update_options = [
                    f"{service['service_id']} - {service['service_name']}"
                    for service in services
                ]

                selected_update = st.selectbox("Choose Service to Update", update_options)
                update_id = selected_update.split(" - ")[0]

                selected_service = None

                for service in services:
                    if service["service_id"] == update_id:
                        selected_service = service
                        break

                if selected_service:
                    new_name = st.text_input(
                        "New Service Name",
                        value=selected_service["service_name"]
                    )

                    new_price = st.number_input(
                        "New Service Price",
                        min_value=0,
                        value=int(selected_service["price"]),
                        step=5
                    )

                    new_duration = st.selectbox(
                        "New Duration",
                        ["30 mins", "1 hour", "1.5 hours", "2 hours"]
                    )

                    if st.button("Update Service"):
                        selected_service["service_name"] = new_name
                        selected_service["price"] = new_price
                        selected_service["duration"] = new_duration

                        save_services()
                        st.success("Service updated successfully!")
                        st.rerun()

            st.divider()
            st.markdown("### Delete Service")

            if len(services) > 0:
                delete_options = [
                    f"{service['service_id']} - {service['service_name']}"
                    for service in services
                ]

                selected_delete = st.selectbox("Choose Service to Delete", delete_options)

                if st.button("Delete Service"):
                    delete_id = selected_delete.split(" - ")[0]

                    services[:] = [
                        service for service in services
                        if service["service_id"] != delete_id
                    ]

                    save_services()
                    st.success("Service deleted successfully!")
                    st.rerun()

        # -------- MANAGE TIME SLOTS --------
        with admin_tab2:
            st.markdown("### Manage Available Time Slots")

            if len(services) > 0:
                service_options = [
                    f"{service['service_id']} - {service['service_name']}"
                    for service in services
                ]

                selected_service = st.selectbox("Choose Service", service_options)
                service_id = selected_service.split(" - ")[0]

                slot_date = st.date_input("Choose Slot Date", min_value=date.today())
                slot_time = st.selectbox(
                    "Choose Slot Time",
                    ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"]
                )

                new_slot = f"{slot_date} {slot_time}"

                if st.button("Add Time Slot"):
                    for service in services:
                        if service["service_id"] == service_id:
                            if new_slot not in service["available_slots"]:
                                service["available_slots"].append(new_slot)
                                save_services()
                                st.success("Time slot added successfully!")
                                st.rerun()
                            else:
                                st.error("That time slot already exists.")
                            break

                st.divider()
                st.markdown("### Remove Existing Slot")

                selected_service_data = None

                for service in services:
                    if service["service_id"] == service_id:
                        selected_service_data = service
                        break

                if selected_service_data and len(selected_service_data["available_slots"]) > 0:
                    remove_slot = st.selectbox(
                        "Select Slot to Remove",
                        selected_service_data["available_slots"]
                    )

                    if st.button("Delete Time Slot"):
                        selected_service_data["available_slots"].remove(remove_slot)
                        save_services()
                        st.success("Time slot deleted successfully!")
                        st.rerun()
                else:
                    st.info("No slots available for this service yet.")

            st.markdown("### Services with Slots")
            st.dataframe(services)

        # -------- VIEW BOOKINGS --------
        with admin_tab3:
            st.markdown("### Client Bookings")
            st.dataframe(bookings)

            st.divider()
            st.markdown("### Mark Appointment as Completed")

            booking_options = [
                f"{booking['booking_id']} - {booking['service_name']} - {booking['appointment_time']}"
                for booking in bookings
                if booking["status"] == "Booked"
            ]

            if len(booking_options) > 0:
                selected_booking = st.selectbox("Select Booking", booking_options)
                stylist_name = st.text_input("Completed By")

                if st.button("Mark as Completed"):
                    if stylist_name.strip() == "":
                        st.error("Please enter who completed the service.")
                    else:
                        booking_id = selected_booking.split(" - ")[0]

                        for booking in bookings:
                            if booking["booking_id"] == booking_id:
                                booking["status"] = "Completed"
                                booking["completed_by"] = stylist_name
                                break

                        save_bookings()
                        st.success("Appointment marked as completed!")
                        st.rerun()
            else:
                st.info("There are no active booked appointments to complete.")

        # -------- REVENUE DASHBOARD --------
        with admin_tab4:
            st.subheader("Revenue Dashboard")

            total_revenue = 0
            completed_count = 0
            cancelled_count = 0
            booked_count = 0

            for booking in bookings:
                if booking["status"] == "Completed":
                    total_revenue += booking.get("price", 0)
                    completed_count += 1
                elif booking["status"] == "Cancelled":
                    cancelled_count += 1
                elif booking["status"] == "Booked":
                    booked_count += 1

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Revenue", f"${total_revenue}")

            with col2:
                st.metric("Completed Appointments", completed_count)

            with col3:
                st.metric("Cancelled Appointments", cancelled_count)

            st.metric("Currently Booked", booked_count)

            revenue_by_service = {}

            for booking in bookings:
                if booking["status"] == "Completed":
                    service_name = booking["service_name"]
                    revenue_by_service[service_name] = revenue_by_service.get(service_name, 0) + booking.get("price", 0)

            if len(revenue_by_service) > 0:
                st.markdown("### Revenue by Service")
                st.bar_chart(revenue_by_service)
            else:
                st.info("No completed appointments yet, so revenue chart is empty.")

        # -------- SEARCH BOOKINGS --------
        with admin_tab5:
            st.subheader("Search Bookings")

            search_email = st.text_input("Search by Client Email")
            search_service = st.text_input("Search by Service")
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Booked", "Completed", "Cancelled"]
            )

            filtered_bookings = bookings

            if search_email:
                filtered_bookings = [
                    booking for booking in filtered_bookings
                    if search_email.lower() in booking["client_email"].lower()
                ]

            if search_service:
                filtered_bookings = [
                    booking for booking in filtered_bookings
                    if search_service.lower() in booking["service_name"].lower()
                ]

            if status_filter != "All":
                filtered_bookings = [
                    booking for booking in filtered_bookings
                    if booking["status"] == status_filter
                ]

            st.dataframe(filtered_bookings)

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
                service_options = [
                    f"{service['service_id']} - {service['service_name']} (${service['price']})"
                    for service in services
                ]

                selected_service = st.selectbox("Choose a Service", service_options)
                selected_service_id = selected_service.split(" - ")[0]

                selected_service_name = ""
                selected_service_price = 0
                selected_service_slots = []

                for service in services:
                    if service["service_id"] == selected_service_id:
                        selected_service_name = service["service_name"]
                        selected_service_price = service["price"]
                        selected_service_slots = service["available_slots"]
                        break

                appointment_date = st.date_input(
                    "Choose Appointment Date",
                    min_value=date.today()
                )

                appointment_time = st.selectbox(
                    "Choose Appointment Time",
                    ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"]
                )

                full_appointment_time = f"{appointment_date} {appointment_time}"

                already_booked = False

                for booking in bookings:
                    if (
                        booking["appointment_time"] == full_appointment_time
                        and booking["status"] == "Booked"
                    ):
                        already_booked = True
                        break

                if already_booked:
                    st.warning("This appointment time is already booked. Please choose another time.")

                if st.button("Book Appointment"):
                    if already_booked:
                        st.error("That time is already booked.")
                    else:
                        new_booking = {
                            "booking_id": str(len(bookings) + 1),
                            "client_name": current_user["full_name"],
                            "client_email": current_user["email"],
                            "service_name": selected_service_name,
                            "price": selected_service_price,
                            "appointment_time": full_appointment_time,
                            "status": "Booked",
                            "completed_by": "",
                            "cancel_reason": ""
                        }

                        bookings.append(new_booking)
                        save_bookings()

                        st.success("Appointment booked successfully!")
                        st.rerun()
            else:
                st.error("No services are available right now.")

        with client_tab3:
            st.markdown("### My Bookings")

            my_bookings = [
                booking for booking in bookings
                if booking["client_email"] == current_user["email"]
            ]

            st.dataframe(my_bookings)

            active_bookings = [
                booking for booking in my_bookings
                if booking["status"] == "Booked"
            ]

            if len(active_bookings) > 0:
                cancel_options = [
                    f"{booking['booking_id']} - {booking['service_name']} - {booking['appointment_time']}"
                    for booking in active_bookings
                ]

                cancel_choice = st.selectbox("Select Booking to Cancel", cancel_options)
                cancel_reason = st.text_input("Reason for Cancellation")

                if st.button("Cancel Booking"):
                    if cancel_reason.strip() == "":
                        st.error("Please enter a reason for cancellation.")
                    else:
                        booking_id = cancel_choice.split(" - ")[0]

                        for booking in bookings:
                            if booking["booking_id"] == booking_id:
                                booking["status"] = "Cancelled"
                                booking["cancel_reason"] = cancel_reason
                                break

                        save_bookings()
                        st.success("Booking cancelled successfully!")
                        st.rerun()
            else:
                st.info("You do not have any active bookings.")

# ---------------- AI CONSULTATION ----------------
elif st.session_state.logged_in and page == "AI Consultation":
    st.subheader("AI Styling & Booking Assistant")

    st.write(
        "Ask the AI assistant a question about your hair, skin, style goals, occasion, or what service you should book."
    )

    with st.container(border=True):
        customer_question = st.text_area(
            "Type your question here:",
            placeholder="Example: I have oily skin and want soft glam for graduation pictures. What should I book?"
        )

        if st.button("Ask AI"):
            if not customer_question:
                st.error("Please type a question first.")
            else:
                st.info(
                    "AI connection goes here. If your separate ai_service.py is working, connect this button to your chatbot function."
                )

    st.divider()

    st.subheader("Available Services")
    st.dataframe(services)

# ---------------- LOGOUT ----------------
elif st.session_state.logged_in and page == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("You have been logged out.")
    st.rerun()