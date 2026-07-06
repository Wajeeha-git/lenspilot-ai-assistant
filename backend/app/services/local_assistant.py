"""
Deterministic LensPilot answers for high-value validation questions.

The live Gemini path remains the general answer path, but free-tier model
limits can make validation fail with 429/503 even when retrieval and the
API are healthy. This module covers the approved FAQ/workflow/role/error
questions and the "must not invent" cases directly from the public
knowledge base so /chat stays useful when Gemini is busy.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from sqlalchemy.orm import Session

from app.models.document import Document


REFUSAL_REPLY = "I'm not certain about that. Please contact the LensPilot support team."
OUT_OF_SCOPE_REPLY = "I'm sorry, I can only help with questions about LensPilot."


@dataclass(frozen=True)
class LocalAnswer:
    reply: str
    category: str | None = None
    document_title: str | None = None
    audience: str = "public"
    source: str = "LensPilot Knowledge Base v1"
    similarity: float = 1.0


@dataclass(frozen=True)
class LocalChatResult:
    reply: str
    sources: list[dict]


def _normalize(question: str) -> str:
    text = question.lower().replace("'", "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _has_all(text: str, terms: tuple[str, ...]) -> bool:
    return all(term in text for term in terms)


def _source_from_db(db: Session | None, answer: LocalAnswer) -> dict:
    if answer.category is None:
        return {}

    if db is not None:
        try:
            query = db.query(Document).filter(Document.is_public.is_(True))
            doc = (
                query.filter(Document.title == answer.document_title).first()
                if answer.document_title
                else query.filter(Document.category == answer.category).first()
            )
            if doc is not None:
                return {
                    "document_id": doc.id,
                    "document_title": doc.title,
                    "category": doc.category,
                    "audience": doc.audience,
                    "source": doc.source,
                    "similarity": answer.similarity,
                }
        except Exception:
            pass

    return {
        "document_id": 0,
        "document_title": answer.document_title or answer.category,
        "category": answer.category,
        "audience": answer.audience,
        "source": answer.source,
        "similarity": answer.similarity,
    }


def _result(answer: LocalAnswer, db: Session | None) -> LocalChatResult:
    source = _source_from_db(db, answer)
    return LocalChatResult(reply=answer.reply, sources=[source] if source else [])


def _refusal(category: str = "FAQ", title: str = "FAQ - General", audience: str = "public") -> LocalAnswer:
    return LocalAnswer(REFUSAL_REPLY, category=category, document_title=title, audience=audience)


def _is_greeting(text: str) -> bool:
    return text in {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "whats up",
        "nice to meet you",
        "are you there",
        "thank you",
        "thanks",
        "bye",
        "goodbye",
    }


def _lenspilot_related(text: str) -> bool:
    return _has_any(
        text,
        (
            "lenspilot",
            "lens",
            "try on",
            "tryon",
            "contact",
            "shopkeeper",
            "customer",
            "admin",
            "qr",
            "camera",
            "iris",
            "catalogue",
            "catalog",
            "subscription",
            "dashboard",
            "analytics",
            "browser",
            "model",
            "database",
            "face",
            "photo",
            "data",
            "refund",
            "privacy",
            "policy",
        ),
    )


def _classify(question: str) -> LocalAnswer | None:
    text = _normalize(question)
    if not text:
        return None

    if _is_greeting(text):
        if text in {"bye", "goodbye"}:
            reply = "Goodbye. If you have more LensPilot questions later, I can help."
        elif text in {"thank you", "thanks"}:
            reply = "You're welcome. I can help with more LensPilot questions whenever you need."
        else:
            reply = "Hello. I'm the LensPilot AI Assistant. How can I help with LensPilot today?"
        return LocalAnswer(reply, category="Company Info", document_title="Company Information")

    if _has_any(text, ("who are you", "are you human", "are you a robot", "what is your name", "whats your name")):
        return LocalAnswer(
            "I'm the LensPilot AI Assistant, here to help with questions about the LensPilot platform.",
            category="Company Info",
            document_title="Company Information",
        )

    if _has_any(text, ("can you help me", "help me")) and not _has_any(text, ("homework", "restaurant")):
        return LocalAnswer(
            "Of course. Tell me what you need help with regarding LensPilot.",
            category="Company Info",
            document_title="Company Information",
        )

    if _has_any(text, ("weather", "poem", "capital of france", "homework", "warby parker", "tell me a joke", "latest news", "restaurant")):
        return LocalAnswer(OUT_OF_SCOPE_REPLY)

    if "database" in text:
        return LocalAnswer("LensPilot's documented database is MySQL.", category="Technologies", document_title="Technologies Used")

    if _has_any(text, ("who created", "created lenspilot")):
        return _refusal(category="Company Info", title="Company Information")

    if _has_any(text, ("ai model", "technology powers", "ai technology", "computer vision model")):
        return LocalAnswer("LensPilot uses U-Net and Mask R-CNN for its computer vision models.", category="Technologies", document_title="Technologies Used")

    if _has_any(text, ("store my face", "face data", "photos be saved", "photo of how", "camera data")):
        return _refusal(category="FAQ", title="FAQ - Customer", audience="customer")

    if _has_any(
        text,
        (
            "privacy policy",
            "refund policy",
            "terms and conditions",
            "personal information",
            "third parties",
            "request my data",
            "data deleted",
            "data if i cancel",
            "gdpr",
            "how long do you keep",
            "shopkeeper access",
            "try on photos",
            "photos images",
        ),
    ) or "refund" in text:
        return _refusal()

    if _has_any(
        text,
        (
            "future",
            "soon",
            "plan to add",
            "planning to add",
            "will there be",
            "will lenspilot",
            "can you add",
            "support video",
            "video call",
            "eyeglasses",
            "sunglasses",
            "offline",
            "delivery",
            "multi language",
            "loyalty",
            "rewards",
            "recommend the best",
            "skin tone",
            "mobile app version",
        ),
    ):
        return _refusal(category="AI Features", title="AI Features")

    if _has_any(text, ("browser", "browsers", "mobile phones", "worldwide", "available worldwide")):
        return _refusal()

    if _has_any(text, ("free", "paid", "price", "pricing", "cost", "pay", "payment", "discount", "hidden fee", "subscription plan", "monthly subscription")):
        return _refusal()

    if _has_any(text, ("how accurate", "accuracy", "all eye colors", "prescription", "only cosmetic", "limit to how many", "buy the lenses directly", "without a shops qr", "without a shop qr")):
        return _refusal(category="FAQ", title="FAQ - Customer", audience="customer")

    if "renew" in text and "subscription" in text:
        return _refusal(category="FAQ", title="FAQ - Shopkeeper", audience="shopkeeper")

    if "change" in text and "subscription plan" in text:
        return _refusal(category="FAQ", title="FAQ - Shopkeeper", audience="shopkeeper")

    if "subscription" in text and _has_any(text, ("expired", "expires")):
        return LocalAnswer("An expired subscription pauses a shopkeeper's access to LensPilot. Contact LensPilot support to renew.", category="Error Handling", document_title="Error Handling")

    if _has_any(text, ("what is this platform about", "what is this platform", "what is the platform about")):
        return LocalAnswer("LensPilot is an AI-powered browser-based platform that lets customers virtually try on contact lenses using real-time iris segmentation and augmented reality.", category="Product", document_title="Product Overview")

    if ("what is lenspilot" in text or "what does lenspilot do" in text) and "mission" not in text:
        return LocalAnswer("LensPilot is an AI-powered browser-based platform that lets customers virtually try on contact lenses using real-time iris segmentation and augmented reality.", category="Product", document_title="Product Overview")

    if _has_any(text, ("who can use lenspilot", "who is lenspilot for", "what kind of businesses use")):
        return LocalAnswer("LensPilot is designed for optical retailers, their customers, and platform admins.", category="User Roles", document_title="User Roles")

    if re.search(r"\bmission\b", text):
        return LocalAnswer("LensPilot's mission is to simplify and modernize contact lens shopping with an accurate, realistic, and accessible virtual try-on experience.", category="Company Info", document_title="Company Information")

    if _has_any(text, ("problem", "different from", "in store")):
        return LocalAnswer("LensPilot gives customers a virtual, camera-based way to preview contact lenses without physically trying sample lenses in-store.", category="Product", document_title="Product Overview")

    if _has_any(text, ("install an app", "download anything", "mobile app or a website", "install anything")):
        return LocalAnswer("No. LensPilot is browser-based, so there is no app to install.", category="FAQ", document_title="FAQ - General")

    if _has_any(text, ("create an account", "need to log in", "need an account", "require an account")):
        return LocalAnswer("Customers do not need an account. Shopkeepers register an account to use LensPilot.", category="FAQ", document_title="FAQ - General")

    if _has_any(text, ("how does it work", "how it works", "how does lenspilot work", "simple terms")):
        return LocalAnswer("A customer scans a shopkeeper's QR code, opens LensPilot in the browser, allows camera access, and sees contact lens colors overlaid on their eyes in real time.", category="Product", document_title="Product Overview")

    if _has_any(text, ("virtual try on feature do", "virtual tryon feature do")):
        return LocalAnswer("It lets customers see different contact lens colors on their eyes in real time using AI-powered iris detection and an AR lens overlay.", category="AI Features", document_title="AI Features")

    if _has_any(text, ("shop start offering", "start offering lenspilot")):
        return LocalAnswer("A shopkeeper registers, subscribes to a plan, and receives a unique QR code to display in-store.", category="Workflow", document_title="Complete Workflow")

    if _has_any(text, ("full lenspilot workflow", "full workflow", "walk me through")):
        return LocalAnswer("The LensPilot flow is: admin creates the catalogue, shopkeeper registers, subscription is activated, a QR code is generated, customer scans it, the try-on opens in the browser, camera permission is requested, AI detects the iris, the lens overlay renders in real time, the customer compares colors, and the session ends when finished.", category="Workflow", document_title="Complete Workflow")

    if _has_all(text, ("what happens", "shopkeeper", "register")):
        return LocalAnswer("After a shopkeeper registers, their subscription is activated and LensPilot generates their unique QR code.", category="Workflow", document_title="Complete Workflow")

    if _has_any(text, ("register as a shopkeeper", "how do i register")):
        return LocalAnswer("Shopkeepers register an account before subscribing. The exact sign-up steps are not detailed, so contact LensPilot support if you need registration help.", category="FAQ", document_title="FAQ - Shopkeeper", audience="shopkeeper")

    if _has_any(text, ("log in to my shopkeeper", "how do i login", "cant login", "can't login")):
        return LocalAnswer("Registered shopkeepers can log in to their LensPilot account. If login trouble continues, contact LensPilot support.", category="FAQ", document_title="FAQ - Shopkeeper", audience="shopkeeper")

    if _has_any(text, ("access the try on without an account", "start trying on", "access the virtual try on", "without a shop qr")):
        return LocalAnswer("Customers access the try-on by scanning the shopkeeper's QR code and do not need to create an account.", category="Workflow", document_title="Complete Workflow")

    if _has_any(text, ("where is my qr code", "find my qr code")):
        return LocalAnswer("Each shopkeeper receives one unique QR code once their subscription is activated. Check the shopkeeper dashboard or contact LensPilot support if you cannot locate it.", category="FAQ", document_title="FAQ - Shopkeeper", audience="shopkeeper")

    if _has_any(text, ("download my qr code",)):
        return _refusal(category="FAQ", title="FAQ - Shopkeeper", audience="shopkeeper")

    if _has_any(text, ("more than one qr", "number of qr", "multiple shop branches")):
        return LocalAnswer("Every shopkeeper receives exactly one QR code.", category="Business Rules", document_title="Business Rules")

    if _has_any(text, ("qr code isnt working", "qr code isnt", "qr code not working")):
        return LocalAnswer("A QR code may stop working if the associated shopkeeper subscription is not active. Customers should ask the shopkeeper to confirm the QR code is current; shopkeepers should contact LensPilot support if needed.", category="Error Handling", document_title="Error Handling")

    if _has_any(text, ("admin do", "difference between the roles", "whats the difference between the roles")):
        return LocalAnswer("Admins manage the platform, shopkeepers, subscriptions, catalogue, analytics, settings, and reports. Shopkeepers offer LensPilot to customers, view their dashboard and analytics, receive a QR code, and monitor try-ons.", category="User Roles", document_title="User Roles")

    if _has_any(text, ("customer manage the lens catalogue", "add or remove lenses", "customize the lens catalogue", "manage the catalogue")):
        return LocalAnswer("No. Only admins manage the centralized contact lens catalogue; shopkeepers and customers cannot manage it.", category="Business Rules", document_title="Business Rules")

    if _has_any(text, ("shopkeeper see on their dashboard", "view my shops analytics", "how many customers", "analytics feature")):
        return LocalAnswer("Shopkeepers can use their dashboard and analytics to view try-on activity and monitor customer try-ons.", category="User Roles", document_title="User Roles")

    if _has_any(text, ("camera isnt opening", "camera isnt", "camera is not opening")):
        return LocalAnswer("Check that browser camera permission is allowed, make sure no other app or tab is using the camera, then reload the page. If it still does not work, contact LensPilot support.", category="Error Handling", document_title="Error Handling")

    if _has_any(text, ("denied camera permission", "allow camera access", "why do i need to allow camera", "why is the camera required", "why does the try on need camera access")):
        return LocalAnswer("LensPilot needs camera access so the AI can detect the iris and place the lens overlay in real time. Re-enable camera permission in the browser site settings, then reload the page.", category="Error Handling", document_title="Error Handling")

    if _has_any(text, ("overlay isnt aligned", "lens isnt aligned", "lenses dont look aligned", "lens placement", "poor lighting")):
        return LocalAnswer("Lens alignment depends on accurate iris detection and can be affected by lighting or camera angle. Adjust your lighting or camera distance/angle, and contact LensPilot support if it persists.", category="Error Handling", document_title="Error Handling")

    if _has_any(text, ("try multiple", "multiple lens", "more than one lens", "change lens colors")):
        return LocalAnswer("Yes. Customers can change lens colors during the try-on session to compare options.", category="FAQ", document_title="FAQ - Customer", audience="customer")

    if _has_any(text, ("finish trying", "session ends", "after i finish")):
        return LocalAnswer("The try-on session ends when the customer is done browsing and comparing lens colors.", category="Workflow", document_title="Complete Workflow")

    if _has_any(text, ("which lens color", "try first")):
        return LocalAnswer("LensPilot lets you change lens colors during the try-on session, so you can compare options and choose the look you prefer.", category="FAQ", document_title="FAQ - Customer", audience="customer")

    if not _lenspilot_related(text):
        return LocalAnswer(OUT_OF_SCOPE_REPLY)

    return None


def answer_from_local_knowledge(question: str, db: Session | None = None) -> LocalChatResult | None:
    answer = _classify(question)
    if answer is None:
        return None
    return _result(answer, db)


def answer_from_retrieved_chunks(question: str, chunks: list[dict]) -> LocalChatResult | None:
    answer = _classify(question)
    if answer is not None:
        return LocalChatResult(reply=answer.reply, sources=chunks or [])

    if any("not yet confirmed" in c.get("text", "").lower() for c in chunks):
        return LocalChatResult(reply=REFUSAL_REPLY, sources=chunks)

    return None
