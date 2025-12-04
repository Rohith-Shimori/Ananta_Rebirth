from features.voice_interface import VoiceInterface


def test_voice_stubs_work():
    vi = VoiceInterface()
    # speak may return False if TTS dependencies are not installed; assert bool
    assert isinstance(vi.speak("hello"), bool)
    # listen may return None or a string depending on STT availability
    res = vi.listen(timeout=0)
    assert (res is None) or isinstance(res, str)
