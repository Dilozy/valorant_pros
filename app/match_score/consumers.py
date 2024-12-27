import json
import asyncio

import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer

from pro_players.models import Team  # Импортируйте вашу модель Team


class MatchScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.team_slug = self.scope['url_route']['kwargs']['team_slug']
        self.is_connected = True  # Флаг для остановки фонового цикла при отключении клиента
        await self.accept()

        # Запускаем фоновую задачу для обновления данных
        self.update_task = asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self, close_code):
        # Завершаем фоновую задачу при отключении
        self.is_connected = False
        if hasattr(self, "update_task"):
            self.update_task.cancel()

    async def receive(self, text_data):
        # Обработка сообщений от клиента (если требуется)
        pass

    async def send_periodic_updates(self):
        """Фоновый цикл для отправки обновлений клиенту."""
        while self.is_connected:
            team = await self.get_team_by_slug(self.team_slug)
            if not team:
                await self.send(text_data=json.dumps({
                    "status": "Team not found"
                }))
                break  # Прерываем цикл, если команда не найдена

            target_team_name = team.name

            # Асинхронный запрос к API
            VLR_API_endpoint = "https://vlrggapi.vercel.app/match?q=live_score"
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(VLR_API_endpoint, timeout=3) as response:
                        if response.status == 200:
                            matches_data_json = (await response.json()).get("data", {}).get("segments", [])
                        else:
                            matches_data_json = []
                except Exception as e:
                    print(f"Error fetching API data: {e}")
                    matches_data_json = []

            # Обработка данных API
            if matches_data_json:
                for live_match in matches_data_json:
                    if target_team_name in (live_match.get("team1"), live_match.get("team2")):
                        await self.send(text_data=json.dumps({
                            "status": 'success',
                            "team1": live_match.get("team1"),
                            "team2": live_match.get("team2"),
                            "team1_score": live_match.get("score1"),
                            "team2_score": live_match.get("score2"),
                            "team1_current_map_score": live_match.get("team1_round_ct", 0) + live_match.get("team1_round_t", 0),
                            "team2_current_map_score": live_match.get("team2_round_ct", 0) + live_match.get("team2_round_t", 0),
                            "match_event": live_match.get("match_event"),
                        }))
                        break  # Отправляем только данные соответствующего матча
                    else:
                        await self.send(text_data=json.dumps({
                            "status": "There is no a live match for this team right now"
                        }))

            # Задержка перед следующим обновлением
            await asyncio.sleep(5)

    async def get_team_by_slug(self, slug):
        """Асинхронный метод для получения команды по slug."""
        try:
            return await Team.objects.aget(slug=slug)
        except Team.DoesNotExist:
            return None