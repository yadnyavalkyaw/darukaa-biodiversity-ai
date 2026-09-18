"""Tests for conversational intelligence, memory accumulation, and clarifying inquiries."""

from darukaa.dialogue import ClarificationEngine, ParameterExtractor, SessionStore
from darukaa.engine import EnvironmentalState


def test_parameter_extractor_text_parsing():
    extractor = ParameterExtractor()
    state = EnvironmentalState()

    text = "My land has soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid"
    state, extracted = extractor.extract_from_text(state, text)

    assert state.soil.organic_carbon_pct == 0.3
    assert state.climate.rainfall_category == "low"
    assert "monoculture" in state.land_use.crop_system
    assert state.region_name == "semi-arid"
    assert len(extracted) >= 3


def test_clarifying_question_on_incomplete_input():
    """Validates:

    User: "Biodiversity is declining on my land"
    System: Asks clarifying questions for SOC, rainfall, and land use.
    """
    clarifier = ClarificationEngine()
    state = EnvironmentalState()  # completely empty

    clarification = clarifier.evaluate_completeness(state)
    assert clarification.is_incomplete is True
    assert "soil_organic_carbon_pct" in clarification.missing_variables
    assert "rainfall_pattern" in clarification.missing_variables
    assert "land_use_type" in clarification.missing_variables
    assert "soil organic carbon %" in clarification.system_response
    assert len(clarification.suggested_quick_replies) > 0


def test_multi_turn_memory_accumulation():
    """Validates that parameters accumulate across turns without loss."""
    session_store = SessionStore()
    extractor = ParameterExtractor()
    clarifier = ClarificationEngine()

    session = session_store.get_or_create("test-multi-turn")

    # Turn 1: Incomplete query
    msg1 = "Biodiversity is declining on my land"
    session.accumulated_state, ext1 = extractor.extract_from_text(
        session.accumulated_state, msg1
    )
    session.add_user_turn(msg1, ext1)
    clarif1 = clarifier.evaluate_completeness(session.accumulated_state)
    assert clarif1.is_incomplete is True

    # Turn 2: Providing SOC
    msg2 = "Soil organic carbon is 0.4%"
    session.accumulated_state, ext2 = extractor.extract_from_text(
        session.accumulated_state, msg2
    )
    session.add_user_turn(msg2, ext2)
    assert session.accumulated_state.soil.organic_carbon_pct == 0.4
    clarif2 = clarifier.evaluate_completeness(session.accumulated_state)
    assert clarif2.is_incomplete is True  # still missing rainfall and land use

    # Turn 3: Providing rainfall and crop
    msg3 = "Rainfall is 350mm, and we grow monoculture wheat"
    session.accumulated_state, ext3 = extractor.extract_from_text(
        session.accumulated_state, msg3
    )
    session.add_user_turn(msg3, ext3)
    assert session.accumulated_state.climate.annual_rainfall_mm == 350.0
    assert "wheat" in session.accumulated_state.land_use.crop_system

    # Should now be complete!
    clarif3 = clarifier.evaluate_completeness(session.accumulated_state)
    assert clarif3.is_incomplete is False
    assert session.accumulated_state.count_active_variables() >= 3
