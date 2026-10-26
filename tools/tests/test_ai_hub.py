import pytest

import ai_hub


def test_available_providers_only_with_keys():
    env = {"GEMINI_API_KEY": "x", "GROQ_API_KEY": "", "OPENROUTER_API_KEY": "y"}
    assert ai_hub.available_providers(env) == ["gemini", "openrouter"]


def test_resolve_order_auto_follows_priority():
    env = {"GROQ_API_KEY": "a", "XAI_API_KEY": "b", "GEMINI_API_KEY": "c"}
    assert ai_hub.resolve_order("auto", env) == ["gemini", "grok", "groq"]


def test_resolve_order_missing_provider_exits():
    with pytest.raises(SystemExit):
        ai_hub.resolve_order("grok", {"GEMINI_API_KEY": "c"})


def test_strip_fences():
    assert ai_hub.strip_fences("```html\n<p>hi</p>\n```") == "<p>hi</p>"
    assert ai_hub.strip_fences("<p>hi</p>") == "<p>hi</p>"


def test_extract_response_text_from_output_items():
    data = {"output": [
        {"type": "x_search_call"},
        {"type": "message", "content": [{"type": "output_text", "text": "答え"}]},
    ]}
    assert ai_hub.extract_response_text(data) == "答え"
    assert ai_hub.extract_response_text({"output_text": "直接"}) == "直接"


def test_load_env_strips_quotes(tmp_path):
    f = tmp_path / ".env"
    f.write_text('# c\nA="1"\nB=2\n', encoding="utf-8")
    assert ai_hub.load_env(f) == {"A": "1", "B": "2"}


def test_new_providers_detected():
    env = {"MISTRAL_API_KEY": "m", "CEREBRAS_API_KEY": "c", "TAVILY_API_KEY": "t"}
    assert ai_hub.available_providers(env) == ["mistral", "cerebras"]
    assert ai_hub.resolve_order("auto", env) == ["mistral", "cerebras"]


def test_format_sources_numbers_and_truncates():
    out = ai_hub.format_sources([{"title": "T", "url": "https://a", "content": "x" * 50}], per_item=10)
    assert out == "[1] T\nURL: https://a\n" + "x" * 10


def test_research_requires_search_key():
    with pytest.raises(SystemExit):
        ai_hub.research("話題", env={"GEMINI_API_KEY": "k"})


def test_research_uses_tavily_when_no_grok(monkeypatch):
    monkeypatch.setattr(ai_hub, "tavily_search", lambda q, env, max_results=8, **o: [{"title": "T", "url": "u", "content": "c"}])
    monkeypatch.setattr(ai_hub, "call", lambda prompt, provider, env: ("gemini", "要約"))
    assert ai_hub.research("話題", env={"TAVILY_API_KEY": "t", "GEMINI_API_KEY": "k"}) == ("tavily+gemini", "要約")


def test_merge_results_dedupes_by_url():
    a = [{"url": "u1"}, {"url": "u2"}]
    b = [{"url": "u2"}, {"url": "u3"}, {"title": "no url"}]
    assert [x["url"] for x in ai_hub.merge_results(a, b)] == ["u1", "u2", "u3"]
