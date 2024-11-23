import pytest
from unittest.mock import patch
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant

from custom_components.dsm import DOMAIN

# Mock input data
MOCK_CONFIG = {
    "api_endpoint": "https://api.example.com",
    "email": "user@example.com",
    "password": "securepassword123",
}


@pytest.fixture
def mock_setup_entry():
    """Mock the async_setup_entry method."""
    with patch(
        "custom_components.dsm.async_setup_entry", return_value=True
    ) as mock_entry_setup:
        yield mock_entry_setup


async def test_config_flow_user_success(hass: HomeAssistant, mock_setup_entry):
    """Test successful user config flow."""
    # Initiate the config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Ensure the form is displayed
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

    # Submit valid user input
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    # Ensure the flow finishes successfully
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == MOCK_CONFIG["api_endpoint"]
    assert result["data"] == MOCK_CONFIG

    # Ensure setup entry was called
    assert len(mock_setup_entry.mock_calls) == 1


async def test_config_flow_invalid_email(hass: HomeAssistant):
    """Test config flow with an invalid email."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Submit invalid email
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "api_endpoint": "https://api.example.com",
            "email": "invalid-email",
            "password": "securepassword123",
        },
    )

    # Ensure the form is re-displayed with an error
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"email": "invalid_email"}


async def test_config_flow_password_too_short(hass: HomeAssistant):
    """Test config flow with a password that is too short."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Submit a short password
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            "api_endpoint": "https://api.example.com",
            "email": "user@example.com",
            "password": "123",
        },
    )

    # Ensure the form is re-displayed with an error
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {"password": "password_too_short"}


async def test_options_flow(hass: HomeAssistant, mock_setup_entry):
    """Test options flow for updating the email and password."""
    # Create a mock config entry
    config_entry = config_entries.ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="https://api.example.com",
        data=MOCK_CONFIG,
        source=config_entries.SOURCE_USER,
        entry_id="test",
        unique_id=None,
        options={},
    )
    hass.config_entries._entries.append(config_entry)

    # Initiate the options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    # Ensure the form is displayed
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"

    # Submit updated email and password
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            "email": "newuser@example.com",
            "password": "newsecurepassword",
        },
    )

    # Ensure the options flow finishes successfully
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert config_entry.data["email"] == "newuser@example.com"
    assert config_entry.data["password"] == "newsecurepassword"
