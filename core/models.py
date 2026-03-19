from django.conf import settings
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    class Role(models.TextChoices):
        CLIENT = "client", "Cliente"
        AGENT = "agent", "Agente"
        ADMIN = "admin", "Administrador"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    phone_number = models.CharField(max_length=25, blank=True)

    def __str__(self) -> str:
        return f"{self.user} ({self.get_role_display()})"


class Location(TimeStampedModel):
    district = models.CharField("Distrito", max_length=120)
    city = models.CharField("Cidade", max_length=120)
    neighborhood = models.CharField("Bairro", max_length=120, blank=True)
    postal_code = models.CharField("Código Postal", max_length=20, blank=True)

    class Meta:
        ordering = ["district", "city", "neighborhood"]
        unique_together = ("district", "city", "neighborhood", "postal_code")

    def __str__(self) -> str:
        parts = [self.city, self.district]
        if self.neighborhood:
            parts.insert(0, self.neighborhood)
        return " - ".join(parts)


class PropertyType(TimeStampedModel):
    name = models.CharField("Nome", max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Amenity(TimeStampedModel):
    name = models.CharField("Nome", max_length=120, unique=True)
    icon = models.CharField("Ícone", max_length=60, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Property(TimeStampedModel):
    class ListingType(models.TextChoices):
        SALE = "sale", "Venda"
        RENT = "rent", "Arrendamento"

    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        PUBLISHED = "published", "Publicado"
        RESERVED = "reserved", "Reservado"
        SOLD = "sold", "Vendido"
        RENTED = "rented", "Arrendado"

    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="properties")
    title = models.CharField("Título", max_length=180)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField("Descrição")
    listing_type = models.CharField("Tipo de anúncio", max_length=20, choices=ListingType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name="properties")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="properties")

    price = models.DecimalField("Preço", max_digits=12, decimal_places=2)
    condominium_fee = models.DecimalField("Condomínio", max_digits=10, decimal_places=2, null=True, blank=True)
    area_m2 = models.DecimalField("Área (m²)", max_digits=10, decimal_places=2)
    bedrooms = models.PositiveSmallIntegerField("Quartos", default=0)
    bathrooms = models.PositiveSmallIntegerField("Casas de banho", default=1)
    parking_spaces = models.PositiveSmallIntegerField("Lugares de estacionamento", default=0)

    address = models.CharField("Morada", max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["status", "listing_type"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class PropertyImage(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/")
    alt_text = models.CharField(max_length=180, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"Imagem #{self.id} - {self.property.title}"


class Lead(TimeStampedModel):
    class LeadStatus(models.TextChoices):
        NEW = "new", "Novo"
        CONTACTED = "contacted", "Contactado"
        QUALIFIED = "qualified", "Qualificado"
        CLOSED = "closed", "Fechado"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="leads")
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
    )
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=25, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Lead {self.full_name} - {self.property.title}"


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "property"], name="unique_favorite_user_property"),
        ]

    def __str__(self) -> str:
        return f"{self.user} ❤️ {self.property}"
