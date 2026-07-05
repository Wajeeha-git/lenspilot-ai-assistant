"""
Tests for the ingestion pipeline's metadata parsing and chunking logic.
None of these need a live DB or Gemini key -- they test pure functions.
"""
from ingestion.ingest import (
    parse_frontmatter,
    chunk_markdown,
    chunk_text,
    filename_to_title,
    guess_category,
)


SAMPLE_WITH_FRONTMATTER = """---
title: FAQ - Customer
category: FAQ
audience: customer
source: LensPilot Knowledge Base v1
version: 2026-07-03
public: true
---
# FAQ - Customer

## Does LensPilot store my face?
Not yet confirmed.
"""


def test_parse_frontmatter_extracts_all_fields():
    metadata, body = parse_frontmatter(SAMPLE_WITH_FRONTMATTER)
    assert metadata["title"] == "FAQ - Customer"
    assert metadata["category"] == "FAQ"
    assert metadata["audience"] == "customer"
    assert metadata["source"] == "LensPilot Knowledge Base v1"
    assert metadata["version"] == "2026-07-03"
    assert metadata["public"] is True  # coerced from string "true" to a real bool
    assert body.startswith("# FAQ - Customer")
    assert "---" not in body


def test_parse_frontmatter_handles_missing_block():
    metadata, body = parse_frontmatter("# Just a doc\n\nNo frontmatter here.")
    assert metadata == {}
    assert body == "# Just a doc\n\nNo frontmatter here."


def test_parse_frontmatter_coerces_public_false():
    text = "---\npublic: false\n---\nbody"
    metadata, _ = parse_frontmatter(text)
    assert metadata["public"] is False


def test_chunk_markdown_keeps_each_faq_answer_intact():
    body = (
        "# FAQ - General\n\n"
        "## What is LensPilot?\n"
        "LensPilot is a virtual try-on platform.\n\n"
        "## Is LensPilot free?\n"
        "Not yet confirmed. Contact support.\n\n"
        "## Do I need an account?\n"
        "Customers do not need an account.\n"
    )
    chunks = chunk_markdown(body, max_words=380, overlap_words=30)

    # Each question's full answer should live in exactly one chunk -- never
    # split mid-answer just because a size threshold was crossed.
    faq_chunks = [c for c in chunks if c.startswith("## ")]
    assert any("What is LensPilot?" in c and "virtual try-on platform" in c for c in faq_chunks)
    assert any("Is LensPilot free?" in c and "Contact support" in c for c in faq_chunks)
    assert any("Do I need an account?" in c and "do not need an account" in c for c in faq_chunks)


def test_chunk_markdown_subsplits_oversized_section_but_keeps_heading():
    long_answer = " ".join(["word"] * 900)  # forces sub-chunking
    body = f"# Doc\n\n## A very long section\n{long_answer}\n"

    chunks = chunk_markdown(body, max_words=300, overlap_words=20)

    assert len(chunks) > 1
    # every sub-chunk of the oversized section should retain the heading,
    # so retrieval still has topic context even on a split section
    for c in chunks:
        assert c.startswith("## A very long section")


def test_chunk_markdown_falls_back_to_plain_chunking_without_headings():
    body = "Just a plain paragraph with no markdown headings at all, " * 5
    chunks = chunk_markdown(body, max_words=20, overlap_words=5)
    assert len(chunks) > 1
    assert all(isinstance(c, str) and c.strip() for c in chunks)


def test_chunk_markdown_skips_near_empty_leading_title_fragment():
    body = "# Just A Title\n\n## Real Section\nSome real content here.\n"
    chunks = chunk_markdown(body)
    assert not any(c.strip() == "# Just A Title" for c in chunks)
    assert any("Real Section" in c for c in chunks)


def test_chunk_text_overlap_behavior():
    words = [f"w{i}" for i in range(20)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    assert len(chunks) == 3
    # the tail of chunk 0 should reappear at the head of chunk 1 (the overlap)
    assert chunks[0].split()[-3:] == chunks[1].split()[:3]


def test_filename_to_title_fixes_acronyms():
    assert filename_to_title("faq_general.md") == "FAQ General"
    assert filename_to_title("ai_features.md") == "AI Features"
    assert filename_to_title("company_information.md") == "Company Information"


def test_guess_category_matches_new_topic_files():
    assert guess_category("faq_customer.md") == "FAQ"
    assert guess_category("error_handling.md") == "Error Handling"
    assert guess_category("business_rules.md") == "Business Rules"
    assert guess_category("workflow.md") == "Workflow"
    assert guess_category("technologies_used.md") == "Technologies"
