from wordfreq import zipf_frequency
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def score_guess(guess: str, target: str):
    if len(guess) != 5 or len(target) != 5:
        raise ValueError("guess and target must be 5-letter strings")

    result = ['X'] * 5
    remaining = {}

    for ch in target:
        remaining[ch] = remaining.get(ch, 0) + 1

    for i, ch in enumerate(guess):
        if ch == target[i]:
            result[i] = ch
            remaining[ch] -= 1

    for i, ch in enumerate(guess):
        if result[i] != 'X' and result[i] == ch:
            continue
        if remaining.get(ch, 0) > 0:
            result[i] = '?'
            remaining[ch] -= 1

    return ''.join(result)


def is_valid_word(word: str) -> bool:
    if not isinstance(word, str):
        return False

    word = word.strip().lower()
    if len(word) != 5 or not word.isalpha():
        return False

    return zipf_frequency(word, 'en') >= 2.0


# Backward-compatible alias for older calls.
isvalid_word = is_valid_word


@app.get("/validate")
def validate_word(word: str):
    return {"valid": is_valid_word(word)}


@app.get("/score")
def score_word(guess: str, target: str):
    return {"result": score_guess(guess, target)}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("logic:app", host="127.0.0.1", port=8001, reload=False)

    target = 'saint'
    max_guesses = 5
    attempts_used = 0

    while attempts_used < max_guesses:
        guess = input(f'Enter guess {attempts_used + 1}/{max_guesses}: ').lower()
        if len(guess) != 5:
            print('Guess must be 5 letters.')
            continue
        if not is_valid_word(guess):
            print('Not a valid English word.')
            continue

        attempts_used += 1
        print(score_guess(guess, target))

        if guess == target:
            print('You won!')
            break
    else:
        print(f'Out of guesses. Target was: {target}')
