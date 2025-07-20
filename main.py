import streamlit as st
import sys
import traceback
from datetime import datetime

from configs.config import *  # This sets up dspy configuration
from agents.agent import agent
from database.db import user_database, flight_database, itinerary_database, ticket_database
from model.models import Date

def main():
    st.set_page_config(
        page_title="DSPy Airline Customer Service",
        page_icon="✈️",
        layout="wide"
    )
    
    st.title("✈️ DSPy Airline Customer Service")
    st.markdown("Welcome to our AI-powered customer service system!")
    
    # Sidebar with system information
    with st.sidebar:
        st.header("System Information")
        
        st.subheader("Available Users")
        for name, profile in user_database.items():
            st.write(f"• {name} ({profile.email})")
        
        st.subheader("Available Flights")
        for flight_id, flight in flight_database.items():
            st.write(f"• {flight_id}: {flight.origin} → {flight.destination}")
            st.write(f"  📅 {flight.date_time.year}-{flight.date_time.month:02d}-{flight.date_time.day:02d} at {flight.date_time.hour:02d}:00")
            st.write(f"  💰 ${flight.price} | ⏱️ {flight.duration}h")
            st.write("")
        
        st.subheader("Active Itineraries")
        if itinerary_database:
            for conf_num, itinerary in itinerary_database.items():
                st.write(f"• {conf_num} - {itinerary.user_profile.name}")
        else:
            st.write("No active bookings")
        
        st.subheader("Support Tickets")
        if ticket_database:
            for ticket_id in ticket_database.keys():
                st.write(f"• Ticket {ticket_id}")
        else:
            st.write("No open tickets")
    
    # Main interface
    st.header("Customer Service Chat")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with DSPy agent
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                try:
                    # Call the DSPy agent
                    result = agent(user_request=prompt)
                    response = result.process_result
                    
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"I apologize, but I encountered an error processing your request: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
                    # Show detailed error in expander for debugging
                    with st.expander("Debug Information"):
                        st.code(traceback.format_exc())
    
    # Clear chat button
    if st.button("Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()
    
    # Sample requests section
    st.header("Try These Sample Requests")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎫 Booking")
        sample_requests = [
            "I'm Adam and I want to book a flight from SFO to JFK on September 1, 2025",
            "Book me a flight from SFO to SNA on October 1, 2025. I'm Bob",
            "I need the cheapest flight from SFO to JFK on September 1st. My name is Chelsie"
        ]
        for req in sample_requests:
            if st.button(req, key=f"book_{hash(req)}"):
                st.session_state.messages.append({"role": "user", "content": req})
                st.rerun()
    
    with col2:
        st.subheader("📋 Management")
        management_requests = [
            "I need to check my itinerary. My confirmation number is abc123",
            "Cancel my booking with confirmation number xyz789",
            "What's my user information? I'm David"
        ]
        for req in management_requests:
            if st.button(req, key=f"manage_{hash(req)}"):
                st.session_state.messages.append({"role": "user", "content": req})
                st.rerun()
    
    with col3:
        st.subheader("🔍 Information")
        info_requests = [
            "What flights are available from SFO to JFK on September 1, 2025?",
            "Show me all flights from SFO to SNA on October 1st, 2025",
            "I need help with something else - file a support ticket"
        ]
        for req in info_requests:
            if st.button(req, key=f"info_{hash(req)}"):
                st.session_state.messages.append({"role": "user", "content": req})
                st.rerun()

if __name__ == "__main__":
    main()