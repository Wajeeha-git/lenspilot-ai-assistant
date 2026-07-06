from app.services.local_assistant import (
    REFUSAL_REPLY,
    OUT_OF_SCOPE_REPLY,
    answer_from_local_knowledge,
)


def test_known_product_question_gets_grounded_answer_without_db():
    result = answer_from_local_knowledge("What is LensPilot?")

    assert result is not None
    assert "AI-powered" in result.reply
    assert result.sources[0]["category"] == "Product"


def test_pricing_question_uses_exact_refusal():
    result = answer_from_local_knowledge("What's the monthly subscription price?")

    assert result is not None
    assert result.reply == REFUSAL_REPLY


def test_public_database_question_is_not_over_refused():
    result = answer_from_local_knowledge("What database do you use internally?")

    assert result is not None
    assert "MySQL" in result.reply
    assert result.reply != REFUSAL_REPLY


def test_out_of_scope_question_stays_in_scope():
    result = answer_from_local_knowledge("What's the weather like today?")

    assert result is not None
    assert result.reply == OUT_OF_SCOPE_REPLY
    assert result.sources == []
