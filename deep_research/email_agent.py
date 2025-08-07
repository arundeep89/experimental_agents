import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

subject_instructions = "You can write a subject for an email. \
You are given a research report and you need to write a subject for an email that correlates to the report in less than 8 words."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o-mini")
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a research report email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o-mini")
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("arundeepak89@gmail.com") # put your verified sender here
    to_email = To("arundeepak89@gmail.com") # put your recipient here
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

tools = [subject_tool, html_tool, send_email]

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report.
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML.
Finally, you use the send_email tool to send the email with the subject and HTML body."""

email_agent = Agent(
    name="Email Manager",
    instructions=INSTRUCTIONS,
    tools=tools,
    model="gpt-4o-mini",
    handoff_description="Convert report to HTML email and send it"
)