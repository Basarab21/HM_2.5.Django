from django.http import HttpResponse
from django.shortcuts import redirect
import random
from django.middleware.csrf import get_token

MIN_NUM = 1
MAX_NUM = 100


def get_game_state(session):
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(MIN_NUM, MAX_NUM)

    message = session.pop('message', f"Вгадайте число від {MIN_NUM} до {MAX_NUM}.")

    return session['secret_number'], message


def guess_view(request):
    secret_number, message = get_game_state(request.session)

    if request.method == 'POST':
        try:
            user_guess = int(request.POST.get('guess', ''))
            if user_guess < secret_number:
                request.session['message'] = f"Ні, загадане число БІЛЬШЕ, ніж {user_guess}."
            elif user_guess > secret_number:
                request.session['message'] = f"Ні, загадане число МЕНШЕ, ніж {user_guess}."
            else:
                request.session[
                    'message'] = f"🔥 Вітаємо! Ви вгадали число {secret_number}! Почніть <a href='/guess/reset/'>нову гру</a>."

            return redirect('guess_game')

        except ValueError:
            request.session['message'] = "❌ Будь ласка, введіть дійсне число."
            return redirect('guess_game')


    csrf_token = get_token(request)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Вгадай число</title></head>
    <body>
        <h1>❓ Гра: Вгадай число</h1>

        <p style="font-size: 1.2em; font-weight: bold; color: {'green' if 'Вітаємо' in message else 'red' if '❌' in message else 'blue'};">
            {message}
        </p>

        <form method="POST" action="">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <label for="guess">Ваше число:</label>
            <input type="number" id="guess" name="guess" min="{MIN_NUM}" max="{MAX_NUM}" required autofocus>
            <button type="submit">Спробувати</button>
        </form>

        <p><a href='/guess/reset/'>Почати нову гру</a></p>

        </body>
    </html>
    """

    return HttpResponse(html_content)


def reset_game_view(request):
    if 'secret_number' in request.session:
        del request.session['secret_number']
    if 'message' in request.session:
        del request.session['message']

    request.session['message'] = "Нову гру розпочато! 🎉"

    return redirect('guess_game')