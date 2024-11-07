import re
from django import forms

# форма оформления заказа
class CreateOrderForm(forms.Form):

    first_name = forms.CharField() # имя
    last_name = forms.CharField() # фамилия
    phone_number = forms.CharField() # номер телефона
    
    # способ доставки (доставка или самовывоз)
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
            ],
        )
    
    # адрес доставки
    delivery_address = forms.CharField(required=False)
    
    # способ оплаты (картой или наличными)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
            ],
        )

    # проверка номера телефона
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number'] # номер телефона из формы

        if not data.isdigit(): # если в номере телефона есть символы, отличные от цифр
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        
        # шаблон для номера телефона (10 цифр)
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data