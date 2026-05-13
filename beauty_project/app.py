import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime, date

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

# ---------------- HELPER FUNCTIONS ----------------
def save_users():
    with users_path.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def save_services():
    with services_path.open("w", encoding="utf-8") as f:
        json.dump(services, f, indent=4)

def save_bookings():
    with bookings_path.open("w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=4)

def get_ai_response(customer_question, services):
    service_text = ""

    for service in services:
        service_text += (
            f"- {service['service_name']}: "
            f"${service['price']}, "
            f"{service['duration']}\n"
        )

    prompt = f"""
You are an AI beauty booking assistant.

Only recommend services from this service list:
{service_text}

Customer question:
{customer_question}

Answer in a friendly and helpful way. Recommend the best service from the list.
Mention why it fits the customer's needs. Do not make up services that are not listed.
"""


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
                            save_users()

                        st.success("Account created successfully!")

    with col2:
        with st.expander("View User Database"):
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
                if not service_name:
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
                        save_services()

                    st.success("Service added successfully!")

            st.markdown("### Current Services")
            st.dataframe(services)

            st.divider()
            st.markdown("### Update Service")

            if len(services) > 0:
                update_options = []

                for service in services:
                    update_options.append(
                        f"{service['service_id']} - {service['service_name']}"
                    )

                selected_update = st.selectbox("Choose Service to Update", update_options)
                update_id = selected_update.split(" - ")[0]

                selected_service = None

                for service in services:
                    if service["service_id"] == update_id:
                        selected_service = service
                        break

                if selected_service:
                    new_name = st.text_input("New Service Name", value=selected_service["service_name"])
                    new_price = st.number_input("New Service Price", min_value=0, value=int(selected_service["price"]), step=5)
                    new_duration = st.selectbox("New Duration", ["30 mins", "1 hour", "1.5 hours", "2 hours"])

                    if st.button("Update Service"):
                        for service in services:
                            if service["service_id"] == update_id:
                                service["service_name"] = new_name
                                service["price"] = new_price
                                service["duration"] = new_duration
                                break

                        save_services()
                        st.success("Service updated successfully!")

            st.divider()
            st.markdown("### Delete Service")

            if len(services) > 0:
                delete_options = []

                for service in services:
                    delete_options.append(
                        f"{service['service_id']} - {service['service_name']}"
                    )

                selected_delete = st.selectbox("Choose Service to Delete", delete_options)

                if st.button("Delete Service"):
                    delete_id = selected_delete.split(" - ")[0]

                    updated_services = []

                    for service in services:
                        if service["service_id"] != delete_id:
                            updated_services.append(service)

                    services.clear()
                    services.extend(updated_services)
                    save_services()

                    st.success("Service deleted successfully!")
                    st.rerun()

        with admin_tab2:
            st.markdown("### Manage Available Time Slots")

            if len(services) > 0:
                service_options = []

                for service in services:
                    service_options.append(
                        f"{service['service_id']} - {service['service_name']}"
                    )

                selected_service = st.selectbox("Choose Service", service_options)
                service_id = selected_service.split(" - ")[0]

                st.markdown("#### Add New Slot")
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
                            else:
                                st.error("That time slot already exists.")
                            break

                st.markdown("#### Remove Existing Slot")

                selected_service_data = None

                for service in services:
                    if service["service_id"] == service_id:
                        selected_service_data = service
                        break

                if selected_service_data and len(selected_service_data["available_slots"]) > 0:
                    remove_slot = st.selectbox("Select Slot to Remove", selected_service_data["available_slots"])

                    if st.button("Delete Time Slot"):
                        for service in services:
                            if service["service_id"] == service_id:
                                service["available_slots"].remove(remove_slot)
                                save_services()
                                st.success("Time slot deleted successfully!")
                                st.rerun()
                else:
                    st.info("No slots available for this service yet.")

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

                selected_service_name = ""

                for service in services:
                    if service["service_id"] == selected_service_id:
                        selected_service_name = service["service_name"]
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
                    if booking["appointment_time"] == full_appointment_time and booking["status"] == "Booked":
                        already_booked = True
                        break

                if already_booked:
                    st.warning("This appointment time is already booked. Please choose another time.")

                if st.button("Book Appointment"):
                    if already_booked:
                        st.error("That time is already booked.")
                    else:
                        with st.spinner("Booking your appointment..."):
                            time.sleep(2)

                            new_booking = {
                                "booking_id": str(len(bookings) + 1),
                                "client_name": current_user["full_name"],
                                "client_email": current_user["email"],
                                "service_name": selected_service_name,
                                "appointment_time": full_appointment_time,
                                "status": "Booked"
                            }

                            bookings.append(new_booking)
                            save_bookings()

                        st.success("Appointment booked successfully!")

        with client_tab3:
            st.markdown("### My Bookings")

            my_bookings = []

            for booking in bookings:
                if booking["client_email"] == current_user["email"]:
                    my_bookings.append(booking)

            st.dataframe(my_bookings)

            active_bookings = []

            for booking in my_bookings:
                if booking["status"] == "Booked":
                    active_bookings.append(booking)

            if len(active_bookings) > 0:
                cancel_options = []

                for booking in active_bookings:
                    cancel_options.append(
                        f"{booking['booking_id']} - {booking['service_name']} - {booking['appointment_time']}"
                    )

                cancel_choice = st.selectbox("Select Booking to Cancel", cancel_options)

                if st.button("Cancel Booking"):
                    booking_id = cancel_choice.split(" - ")[0]

                    for booking in bookings:
                        if booking["booking_id"] == booking_id:
                            booking["status"] = "Cancelled"
                            break

                    save_bookings()
                    st.success("Booking cancelled successfully!")
                    st.rerun()
            else:
                st.info("You do not have any active bookings.")

# ---------------- AI CONSULTATION ----------------
elif st.session_state.logged_in and page == "AI Consultation":
    current_user = st.session_state.current_user

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
                with st.spinner("AI is thinking..."):
                    answer = get_ai_response(customer_question, services)

                st.success("AI Response")
                st.write(answer)

    st.divider()

    st.subheader("Available Services")
    st.dataframe(services)

# ---------------- LOGOUT ----------------
elif st.session_state.logged_in and page == "Logout":
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("You have been logged out.")
    st.rerun()