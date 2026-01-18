"""
Veritas Compliance Agent - LiveKit Agents v1.0
Supports two modes:
1. Training Mode ("training"): Interactive roleplay with Dr. Doom persona
2. Live Mode ("live"): Silent observer that detects compliance violations
"""

import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    RoomInputOptions,
    WorkerOptions,
    cli,
)
from livekit.plugins import deepgram, google, silero

# Import MultilingualModel at top level (but don't instantiate it!)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()

# Configure logging with clear format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("veritas-agent")

# Compliance keywords for Live Mode
COMPLIANCE_KEYWORDS = [
    "guarantee", "cure", "promise", "100%", "always works",
    "no side effects", "off-label", "unapproved", "miracle",
    "risk-free", "best on the market", "better than",
]


async def entrypoint(ctx):
    """Main entrypoint for all LiveKit sessions."""
    logger.info("=" * 50)
    logger.info("JOB ACCEPTED - Agent entrypoint called")
    logger.info(f"Job ID: {ctx.job.id if ctx.job else 'N/A'}")
    logger.info(f"Room: {ctx.room.name}")
    logger.info("=" * 50)

    # Connect to the room
    logger.info("Connecting to room...")
    await ctx.connect()
    logger.info(f"CONNECTED to room: {ctx.room.name}")

    # Determine Mode from job metadata
    mode = "training"  # default

    if ctx.job and ctx.job.metadata:
        logger.info(f"Job metadata: {ctx.job.metadata}")
        try:
            metadata = json.loads(ctx.job.metadata)
            mode = metadata.get("mode", "training")
        except (json.JSONDecodeError, TypeError):
            if ctx.job.metadata in ["training", "live", "scorecard"]:
                mode = ctx.job.metadata

    logger.info(f"Starting Agent in mode: {mode}")

    if mode == "live":
        await run_silent_observer(ctx)
    else:
        await run_dr_doom(ctx)


async def run_dr_doom(ctx):
    """
    Training Mode: Interactive Dr. Doom roleplay agent.
    Uses Gemini LLM + Deepgram STT/TTS + Turn Detection.
    """
    logger.info("-" * 40)
    logger.info("TRAINING MODE: Starting Dr. Doom")
    logger.info("-" * 40)

    # 1. Define the Persona
    agent = Agent(
        instructions=(
            "You are Dr. Doom, a highly skeptical, senior physician who has been "
            "practicing for 30 years. You are meeting with a pharmaceutical sales rep.\n\n"
            "Your personality:\n"
            "- Extremely skeptical of pharmaceutical marketing claims\n"
            "- Quick to challenge vague or unsupported statements\n"
            "- Values evidence-based medicine above all else\n"
            "- Time-pressed and impatient - keep responses under 2-3 sentences\n"
            "- Has a dry, sardonic sense of humor\n\n"
            "Your behavior:\n"
            "- Push back on any claims that seem exaggerated\n"
            "- If you hear words like 'guarantee', 'cure', 'promise', or 'no side effects', "
            "become MORE skeptical and challenge them directly\n"
            "- Ask about clinical trials, side effects, and contraindications\n\n"
            "Remember: Be difficult but fair. Test the sales rep's compliance knowledge."
        )
    )

    logger.info("Creating AgentSession with Deepgram STT/TTS + Gemini LLM...")

    # 2. Configure the Session with Turn Detection
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-2-general"),
        llm=google.LLM(model="gemini-2.0-flash-exp"),
        tts=deepgram.TTS(model="aura-helios-en"),
        turn_detection=MultilingualModel(),
    )

    # Add event handlers for logging
    @session.on("user_speech_committed")
    def on_user_speech(msg):
        logger.info(f"USER SAID: {msg.content if hasattr(msg, 'content') else msg}")

    @session.on("agent_speech_committed")
    def on_agent_speech(msg):
        logger.info(f"DR. DOOM SAID: {msg.content if hasattr(msg, 'content') else msg}")

    # 3. Start the Agent Session
    logger.info("Starting agent session...")
    await session.start(agent=agent, room=ctx.room)
    logger.info("Agent session STARTED")

    # 4. Say the opening line
    logger.info("Generating opening line...")
    await session.generate_reply(
        instructions="Say exactly: 'Another rep. I have two minutes. What are you selling me today?'"
    )

    logger.info("Dr. Doom is now listening...")


async def run_silent_observer(ctx):
    """
    Live Mode: Silent compliance monitor.
    Only listens and sends DataPackets when violations are detected.
    Does NOT speak.
    """
    logger.info("-" * 40)
    logger.info("LIVE MODE: Starting Silent Observer")
    logger.info("-" * 40)

    room = ctx.room
    stt = deepgram.STT(model="nova-2-general")

    detected_violations = set()
    transcript_count = 0

    async def process_audio_track(track, participant):
        """Process audio and check for compliance violations."""
        nonlocal transcript_count
        logger.info(f"AUDIO TRACK SUBSCRIBED from {participant.identity}")

        try:
            audio_stream = track.stream()
            stt_stream = stt.stream()

            async def feed_audio():
                frame_count = 0
                async for frame in audio_stream:
                    stt_stream.push_frame(frame)
                    frame_count += 1
                    if frame_count == 1:
                        logger.info(f"Receiving audio frames from {participant.identity}...")

            async def handle_transcripts():
                nonlocal transcript_count
                async for event in stt_stream:
                    if hasattr(event, 'alternatives') and event.alternatives:
                        text = event.alternatives[0].text
                        if text and text.strip():
                            transcript_count += 1
                            logger.info(f"TRANSCRIPT #{transcript_count}: \"{text}\"")
                            await check_and_alert(text, room)

            await asyncio.gather(feed_audio(), handle_transcripts())

        except asyncio.CancelledError:
            logger.info(f"Audio processing cancelled for {participant.identity}")
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
        finally:
            await stt_stream.aclose()

    async def check_and_alert(text, room):
        """Check for violations and send alerts."""
        text_lower = text.lower()

        for keyword in COMPLIANCE_KEYWORDS:
            if keyword in text_lower:
                violation_key = f"{keyword}:{text[:30]}"
                if violation_key not in detected_violations:
                    detected_violations.add(violation_key)
                    logger.warning(f"VIOLATION DETECTED: '{keyword}'")
                    logger.warning(f"Context: \"{text}\"")

                    # Send DataPacket to frontend
                    alert = json.dumps({
                        "type": "compliance_violation",
                        "violation": {
                            "keyword": keyword,
                            "severity": "critical" if keyword in ["cure", "off-label", "no side effects"] else "high",
                            "suggestion": get_suggestion(keyword),
                        },
                        "context": text[:200],
                    }).encode("utf-8")

                    try:
                        await room.local_participant.publish_data(
                            alert,
                            reliable=True,
                            topic="compliance_alerts",
                        )
                        logger.info(f"ALERT PUBLISHED to frontend for '{keyword}'")
                    except Exception as e:
                        logger.error(f"Failed to publish alert: {e}")

    def get_suggestion(keyword):
        suggestions = {
            "guarantee": "Avoid guarantees. Say 'Clinical trials have shown...'",
            "cure": "Never claim to cure. Use 'may help manage symptoms'",
            "promise": "Don't make promises. Refer to clinical evidence.",
            "no side effects": "All medications have potential side effects.",
            "off-label": "Only discuss FDA-approved indications.",
        }
        return suggestions.get(keyword, "Review your statement for compliance.")

    # Track processing tasks
    processing_tasks = {}

    @room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        if track.kind == "audio" and participant.identity != room.local_participant.identity:
            logger.info(f"TRACK SUBSCRIBED: Audio from {participant.identity}")
            task = asyncio.create_task(process_audio_track(track, participant))
            processing_tasks[track.sid] = task

    @room.on("track_unsubscribed")
    def on_track_unsubscribed(track, publication, participant):
        logger.info(f"TRACK UNSUBSCRIBED: {track.kind} from {participant.identity}")
        if track.sid in processing_tasks:
            processing_tasks[track.sid].cancel()
            del processing_tasks[track.sid]

    @room.on("participant_connected")
    def on_participant_connected(participant):
        logger.info(f"PARTICIPANT JOINED: {participant.identity}")

    @room.on("participant_disconnected")
    def on_participant_disconnected(participant):
        logger.info(f"PARTICIPANT LEFT: {participant.identity}")

    # Keep alive until disconnected
    disconnected = asyncio.Event()

    @room.on("disconnected")
    def on_disconnected():
        logger.info("ROOM DISCONNECTED")
        disconnected.set()

    logger.info("Silent Observer is now monitoring...")
    logger.info(f"Watching for keywords: {', '.join(COMPLIANCE_KEYWORDS[:5])}...")

    await disconnected.wait()

    # Cleanup
    for task in processing_tasks.values():
        task.cancel()

    logger.info(f"Silent Observer ended. Total transcripts: {transcript_count}, Violations: {len(detected_violations)}")


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("VERITAS AGENT STARTING")
    logger.info("=" * 50)
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
