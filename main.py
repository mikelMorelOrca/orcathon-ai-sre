import dotenv
import os
from textwrap import dedent
from agno.models.aws.bedrock import AwsBedrock,Session
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.agent import Agent
from slack_tools import init_slack_client, get_slack_channels, get_slack_messages, get_slack_thread_replies, get_slack_user_info, get_slack_channel_info, fetch_slack_messages_with_threads, get_slack_client

dotenv.load_dotenv()

AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")    
MODEL = os.getenv("MODEL")

print(AWS_PROFILE, AWS_REGION, MODEL)

init_slack_client(os.getenv("SLACK_BOT_TOKEN"))

session = Session(
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

agent = Agent(
    model=AwsBedrock(session=session,id=MODEL),

    instructions=dedent("""you are a highly trained SRE engineer in Orca Security. You are responsible for monitoring and managing the infrastructure, scans and stability of a company.
    as part of this job you are reving requests coming to a slack channel and suppose to summarize "to the point", make sure to also review replies and ignore irrelevant [not SRE] requests, make sure to understand and describe what was requested, what does it require to do, timestamps, etc.
    for each issue you found go over jira and find a relevant product/feature and corresponding article within the project that matches the request details, providing answers or guide on "how to" for the request. """),
    tools=[DuckDuckGoTools(), get_slack_channels, get_slack_messages, get_slack_thread_replies,get_slack_user_info, get_slack_channel_info, fetch_slack_messages_with_threads ],
    markdown=True,
    additional_context="""Today is 2025-09-16""",
    #debug_mode=False,
    #debug_level=3,
)
agent.print_response("Find the last 10 requests in C076NHGBK8E slack channel . Today is 2025-09-16, look for messages from the past 30 days maximum.")
