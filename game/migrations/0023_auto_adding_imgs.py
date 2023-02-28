from django.db import migrations
from game.models import Category


def add_images(apps, schema_editor):
    """
    Create periodic tasks
    :param apps
    :param schema_editor
    :return: None
    """
    categories = Category.objects.all()
    for cat in categories:
        ph, phb = "", ""
        if cat.id == 20:
            ph="juegos/tarjetas/android_0.jpg"
            phb = "juegos/tarjetas/android.jpg"
        if cat.id == 19:
            ph="juegos/tarjetas/atari_0.jpg"
            phb = "juegos/tarjetas/atari.jpg"
        if cat.id == 18:
            ph="juegos/tarjetas/gameboy_0.jpg"
            phb = "juegos/tarjetas/gameboy.jpg"
        if cat.id == 7:
            ph="juegos/tarjetas/GameBoyAdvance2.jpg"
            phb = "juegos/tarjetas/GameBoyAdvance.jpg"
        if cat.id == 14:
            ph="juegos/tarjetas/GameBoyColor2.jpg"
            phb = "juegos/tarjetas/GameBoyColor.jpg"
        if cat.id == 1:
            ph="juegos/tarjetas/pc-game_0.jpg"
            phb = "juegos/tarjetas/pc-game.jpg"
        if cat.id == 3:
            ph="juegos/tarjetas/mini-game_0.jpg"
            phb = "juegos/tarjetas/mini-game.jpg"
        if cat.id == 5:
            ph="juegos/tarjetas/Nintendo642.jpg"
            phb = "juegos/tarjetas/Nintendo64.jpg"
        if cat.id == 6:
            ph="juegos/tarjetas/NintendoDS2.jpg"
            phb = "juegos/tarjetas/NintendoDS.jpg"
        if cat.id == 10:
            ph="juegos/tarjetas/PlayStation12.jpg"
            phb = "juegos/tarjetas/PlayStation1.jpg"
        if cat.id == 11:
            ph="juegos/tarjetas/PlayStation22.jpg"
            phb = "juegos/tarjetas/PlayStation2.jpg"
        if cat.id == 9:
            ph="juegos/tarjetas/PS32.jpg"
            phb = "juegos/tarjetas/PS3.jpg"
        if cat.id == 17:
            ph="juegos/tarjetas/PS42.jpg"
            phb = "juegos/tarjetas/PS4.jpg"
        if cat.id == 8:
            ph="juegos/tarjetas/PSP2.jpg"
            phb = "juegos/tarjetas/PSP.jpg"
        if cat.id == 13:
            ph="juegos/tarjetas/SEGA2.jpg"
            phb = "juegos/tarjetas/SEGA.jpg"
        if cat.id == 12:
            ph="juegos/tarjetas/Nintendo2.jpg"
            phb = "juegos/tarjetas/Nintendo.jpg"
        if cat.id == 4:
            ph="juegos/tarjetas/Xbox3602.jpg"
            phb = "juegos/tarjetas/Xbox360.jpg"
        if cat.id == 16:
            ph="juegos/tarjetas/XboxOne2.jpg"
            phb = "juegos/tarjetas/XboxOne2.jpg"
                
        cat.photo=ph
        cat.photo_back=phb
        cat.save()
    

class Migration(migrations.Migration):
    dependencies = [
        ('game', '0022_auto_20220302_0503'),
    ]
    operations = [
        migrations.RunPython(add_images),
    ]
