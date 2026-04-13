import html

def format_project_notification(project: dict, employer_stats: str = "") -> str:
    attrs = project.get('attributes', {})
    title = attrs.get('name', 'Без названия')
    budget = attrs.get('budget')
    budget_amount = budget.get('amount', 'Не указан') if budget else 'Не указан'
    currency = budget.get('currency', 'UAH') if budget else 'UAH'
    
    safe_str = "Да" if attrs.get('safe_type') else "Нет"
    skills = attrs.get('skills', [])
    skills_str = ", ".join([s.get('name', '') for s in skills]) if skills else "Не указаны"
    
    employer = attrs.get('employer', {})
    employer_name = f"{employer.get('first_name', '')} {employer.get('last_name', '')}".strip() or employer.get('login', 'Без имени')
    
    desc = attrs.get('description', '')
    if len(desc) > 3000:
        desc = desc[:3000] + "...\n[Полное описание на сайте]"

    msg = (
        f"💼 <b>{html.escape(title)}</b>\n\n"
        f"💰 <b>Бюджет:</b> <code>{budget_amount} {currency}</code>\n"
        f"🛡 <b>Сейф:</b> {safe_str}\n"
        f"🛠 <b>Категории:</b> {html.escape(skills_str)}\n"
        f"👤 <b>Заказчик:</b> {html.escape(employer_name)} <i>{html.escape(employer_stats)}</i>\n\n"
        f"📝 <b>Описание:</b>\n"
        f"<blockquote expandable>{html.escape(desc)}</blockquote>"
    )
    return msg
