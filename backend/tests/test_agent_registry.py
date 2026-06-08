from app.agents.registry import build_default_agent_registry


def test_default_agents_are_registered():
    registry = build_default_agent_registry()
    agent_ids = {agent.definition.agent_id for agent in registry.list_agents()}
    assert "scholarship" in agent_ids
    assert "research" in agent_ids
    assert "memory" in agent_ids


def test_goal_selection_prefers_scholarship_agent():
    registry = build_default_agent_registry()
    agent = registry.select_for_goal("Find MSc scholarships with full funding and deadlines")
    assert agent.definition.agent_id == "scholarship"

