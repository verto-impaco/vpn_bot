from datetime import datetime, timezone
from database.db_session import get_session
from database.models import User, Subscription


def get_user_subscription_info(telegram_id: int) -> dict:
    """
    Возвращает информацию о подписке пользователя.
    Если подписки нет, возвращает словарь с признаком отсутствия.
    """
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            return {"exists": False, "reason": "Пользователь не найден в системе"}

        subscription = session.query(Subscription).filter_by(
            user_telegram_id=telegram_id, is_active=True
        ).first()

        if not subscription:
            return {"exists": False, "reason": "Активная подписка не найдена"}

        # Расчёт оставшихся дней
        days_left = None
        valid_until_value = getattr(subscription, 'valid_until', None)
        if valid_until_value:
            # Добавляем часовой пояс, если его нет
            if subscription.valid_until.tzinfo is None:
                valid_until_aware = subscription.valid_until.replace(
                    tzinfo=timezone.utc)
            else:
                valid_until_aware = subscription.valid_until

            delta = valid_until_aware - datetime.now(timezone.utc)
            days_left = max(0, delta.days)

        return {
            "exists": True,
            "is_active": subscription.is_active,
            "valid_until": subscription.valid_until,
            "days_left": days_left,
            "vpn_config_id": subscription.vpn_config_id
        }
    finally:
        session.close()


def format_subscription_message(info: dict) -> str:
    """Простое форматирование без рамок и прогресс-бара (если нужно)"""
    if not info["exists"]:
        return f"❌ {info['reason']}\n\nОбратитесь к администратору для приобретения подписки."

    msg = "📊 ИНФОРМАЦИЯ О ПОДПИСКЕ\n"
    msg += "═" * 24 + "\n\n"
    msg += f"Статус: {'✅ Активна' if info['is_active'] else '❌ Неактивна'}\n"

    if info["valid_until"]:
        msg += f"Действительна до: {info['valid_until'].strftime('%d.%m.%Y в %H:%M')}\n"

    if info["days_left"] is not None:
        msg += f"Осталось дней: {info['days_left']}\n"
        # Добавляем визуальный индикатор
        if info["days_left"] > 30:
            msg += f"📈 Статус: Отлично\n"
        elif info["days_left"] > 7:
            msg += f"⚠️ Статус: Скоро закончится\n"
        else:
            msg += f"🔴 Статус: Срочно продлите!\n"

    if info["vpn_config_id"]:
        msg += f"\n🔑 ID конфига: {info['vpn_config_id']}\n"

    msg += "\n" + "═" * 24
    return msg
