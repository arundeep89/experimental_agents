from search_agent import search_agent
from planner_agent import planner_agent
from writer_agent import writer_agent
from email_agent import email_agent
import asyncio
from agents import Agent, Runner, trace, gen_trace_id

class ReportManager:
    # Convert agents to tools

    async def run(self, query: str):
        planner_tool = planner_agent.as_tool(tool_name="planner_agent", tool_description="Create search strategy")
        search_tool = search_agent.as_tool(tool_name="search_agent", tool_description="Execute web searches and summarises results")
        writer_tool = writer_agent.as_tool(tool_name="writer_agent", tool_description="Generate research report")
        email_tool = email_agent.as_tool(tool_name="email_agent", tool_description="Generate email subject and body, and send the email")

        MANAGER_INSTRUCTIONS = """
        You are the Research Manager orchestrator.

        1) **Plan.** Once the user asks a query, call PlannerAgent to get a tuned WebSearchPlan.
        2) **Search.** For each item in that plan, call SearchAgent to get summaries.
        3) **Write.** Pass the collected summaries to WriterAgent to produce a full report.
        4) **Email.** Use the send_email tool to format and deliver the report via HTML.

        Make sure each handoff is explicit (you invoke the appropriate tool with the right data).
        """

        tools = [planner_tool, search_tool, writer_tool]
        handoffs = [email_tool]

        report_manager = Agent(
            name="Report Manager",
            instructions=MANAGER_INSTRUCTIONS,
            tools=tools,
            handoffs=handoffs,
            model="gpt-4o-mini")
        
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            result = await Runner.run(report_manager, query)
            yield result.final_output


    