from keyboard.reply_keyboard import worked_tender_markup
from models.data import TenderName
from models.db_model import WorkedTender, TenderOrm
from service.PostgresOrm import PostgresOrm


async def choice_tender(message, state):
    tenders = await PostgresOrm().get_tenders()
    await state.update_data(tenders=tenders)
    tender_names = tender_to_tender_name(tenders)
    text = ''
    for tender in tender_names:
        text += tender.text
    await message.answer(text)
    await state.update_data(tender_names=tender_names)
    await message.answer("Отправьте реестровый номер или ссылку на объект",
                         reply_markup=worked_tender_markup(tender_names))

def tender_to_tender_name(tenders: list[TenderOrm]) -> list[TenderName]:
    tender_names = []
    for tender in tenders:
        text = (f'Название тендера: {tender.name}\n'
                f'Регистрационный номер: {tender.registration_number}\n'
                f'Ссылка на объект: {tender.url}\n'
                f'Дата окончания приема заявок: {tender.end_date}\n\n')
        tender_names.append(TenderName(tender=tender, text=text))
    return tender_names
