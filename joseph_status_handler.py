import json
from pathlib import Path

JOSEPH_STATE_FILE = Path("/srv/dev/joseph_state.json")

async def joseph_status(update, context):
    if not JOSEPH_STATE_FILE.exists():
        await update.message.reply_text("Joseph ainda não possui estado registrado.")
        return

    data = json.loads(JOSEPH_STATE_FILE.read_text())

    events = data.get("events", [])
    last = events[-1] if events else None

    msg = "🧠 Joseph State\n\n"
    msg += f"Versão: {data.get('version')}\n"
    msg += f"Última atualização: {data.get('last_update')}\n\n"

    if last:
        msg += f"Último evento:\n{last['type']} @ {last['timestamp']}"
    else:
        msg += "Nenhum evento registrado ainda."

    await update.message.reply_text(msg)
