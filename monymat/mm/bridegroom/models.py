from django.db import models
from django.utils.translation import ugettext_lazy as _
from core import models as core_models


class Educations(core_models.Base):
    name = models.CharField(_('Higher Degree'), max_length=255, choices=(('MCA', 'MCA'),))

    class Meta:
        db_table = 'educations'
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')

    def __str__(self):
        return self.name


class Religions(core_models.Base):
    name = models.CharField(_('Religion Name'), max_length=255, choices=(('Hindu', 'Hindu'),))

    class Meta:
        db_table = 'religions'
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')

    def __str__(self):
        return self.name


class Stars(core_models.Base):
    name = models.CharField(_('Stars Name'), max_length=255, choices=(('Stars', 'Stars'),))

    class Meta:
        db_table = 'stars'
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')


class Raasis(core_models.Base):
    name = models.CharField(_('Raasi Name'), max_length=255, choices=(('Raasi', 'Raasi'),))

    class Meta:
        db_table = 'raasis'
        verbose_name = _('Raasi')
        verbose_name_plural = _('Raasis')

    def __str__(self):
        return self.name


class Languages(core_models.Base):
    name = models.CharField(_('Language Name'), max_length=255, choices=(('Tamil', 'Tamil'),))

    class Meta:
        db_table = 'languages'
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return self.name


class Gothram(core_models.Base):
    name = models.CharField(_('Gothram Name'), max_length=255, choices=(('Gothram', 'Gothram'),))

    class Meta:
        db_table = 'gothram'
        verbose_name = _('Gothram')
        verbose_name_plural = _('Gothrams')

    def __str__(self):
        return self.name


class Occupations(core_models.Base):
    name = models.CharField(_('Occupations Name'), max_length=255, choices=(('Software Developer', 'Software Developer'),))

    class Meta:
        db_table = 'occupations'
        verbose_name = _('Occupation')
        verbose_name_plural = _('Occupations')

    def __str__(self):
        return self.name


class Casts(core_models.Base):
    name = models.CharField(_('Cast Name'), max_length=255, choices=(('Cast', 'Cast'),))

    class Meta:
        db_table = 'casts'
        verbose_name = _('Cast')
        verbose_name_plural = _('Casts')

    def __str__(self):
        return self.name


class SubCasts(core_models.Base):
    cast = models.ForeignKey(Casts, related_name='sub_casts')
    name = models.CharField(_('SubCast Name'), max_length=255, choices=(('SubCast', 'SubCast'),))

    class Meta:
        db_table = 'subcasts'
        verbose_name = _('SubCast')
        verbose_name_plural = _('SubCasts')

    def __str__(self):
        return self.name



class Country(core_models.Base):
    name = models.CharField(_('Country Name'), max_length=255, choices=(('India', 'India'),))

    class Meta:
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Country')

    def __str__(self):
        return self.name

class State(core_models.Base):
    country = models.ForeignKey(Country, related_name='states')
    name = models.CharField(_('State Name'), max_length=255, choices=(('Tamil Nadu', 'Tamil Nadu'),))

    class Meta:
        db_table = 'state'
        verbose_name = _('State')
        verbose_name_plural = _('State')

    def __str__(self):
        return self.name


class City(core_models.Base):
    state = models.ForeignKey(State, related_name='cities')
    name = models.CharField(_('City Name'), max_length=255, choices=(('Chennai', 'Chennai'),))

    class Meta:
        db_table = 'city'
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return self.name


class Family(core_models.Base):

    user = models.OneToOneField(core_models.User, related_name='family')
    status = models.CharField(_('status'), max_length=255,
                              choices=(('Rich', 'Rich'), ('Upper Middle', 'Upper Middle'), ('Middle', 'Middle')))
    father_name = models.CharField(_('Father name'), max_length=255)
    mother_name = models.CharField(_('Mother name'), max_length=255)

    brother = models.IntegerField(_('Elder Brother'), default=1)
    brother_younger = models.IntegerField(_('Younger Brother'), default=1)
    brother_married = models.IntegerField(_('Number of married Brother'), default=1)

    sister = models.IntegerField(_('Elder Sister'), default=1)
    sister_younger = models.IntegerField(_('Younger Sister'), default=1)
    sister_married = models.IntegerField(_('Number of married Sister'), default=1)

    native_place = models.ForeignKey(City, related_name='family_city')
    cast = models.ForeignKey(Casts, related_name='bridegroom_cast')
    gothram = models.ForeignKey(Gothram, related_name='family_gothram')
    religion = models.ForeignKey(Religions, related_name='family_religion')
    language = models.ForeignKey(Languages, related_name='family_language')
    looking_for = models.CharField(_('Looking for Bride, Groom or both'), choices=(('Bride', 'Bride'),
                                                                                   ('Groom', 'Groom'),
                                                                                   ('Both', 'Both')),
                                   default='Both', max_length=20)

    about = models.TextField(_('About Family'), blank=True, null=True)
    alternate_phone = models.CharField(_('Phone number'), max_length=255, null=True, blank=True)
    phone_number_view_count = models.PositiveIntegerField(_('Number of contacts left till'), default=100)

    class Meta:
        db_table = 'family'
        verbose_name = _('Family')
        verbose_name_plural = _('Families')

    def __str__(self):
        return "%s - %s" % (self.father_name, self.native_place.name)


class BrideGroom(core_models.Base):

    family = models.ForeignKey(Family, related_name='bridegroom_family')
    name = models.CharField(_('Name'), max_length=255)
    about = models.TextField(_('Personal Information'), blank=True, null=True)

    higher_degree = models.ForeignKey(Educations, related_name='bridegroom_education')
    occupations = models.ForeignKey(Occupations, related_name='bridegroom_occupation')
    raasi = models.ForeignKey(Raasis, related_name='bridegroom_raasi')
    star = models.ForeignKey(Stars, related_name='bridegroom_star')

    # gender = models.CharField(_('Gender'), max_length=255, choices=(('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender')))
    gender = models.BooleanField(_('Female=True / Male=False'))
    date_of_birth = models.DateField(_('Date of Birth'))

    living_city = models.ForeignKey(City, related_name='bridegroom_city')

    height = models.FloatField(_('Height in CM'))
    marital_status = models.CharField(_('Marital Status'), max_length=255, choices=(('Single', 'Single'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')), default='Single')
    physical_status = models.BooleanField(_('Physical Status'), default=False)
    complexion = models.CharField(_('Complexion'), max_length=255, choices=(('Dark', 'Dark'), ('Wheatish', 'Wheatish'), ('Fair', 'Fair')))

    drinking = models.BooleanField(_('Drinking Yes or No ?'), default=False)
    smoking = models.BooleanField(_('Smoking Yes or No ?'), default=False)
    employed = models.BooleanField(_('Employed Yes or No?'), default=True)
    income = models.FloatField(_('Annual income'), default=0)

    display_income = models.BooleanField(_('Show Income to all ?'), default=True)
    display_photo = models.BooleanField(_('Show Photo to all ?'), default=True)
    # Only paid members
    only_preferred_star = models.BooleanField(_('Show only to preferred star ?'), default=True)
    only_preferred_cast = models.BooleanField(_('Show only to preferred cast ?'), default=True)
    # Only high profile
    only_preferred_income = models.BooleanField(_('Show only to preferred income range ?'), default=True)
    only_preferred_status = models.BooleanField(_('Show only to preferred family status ?'), default=True)

    is_active = models.BooleanField(_('Is active'), default=True)

    class Meta:
        db_table = 'bridegrooms'
        verbose_name = _('Bride Groom')
        verbose_name_plural = _('Brides Grooms')

    def __str__(self):
        return "%s, %s " % (self.name, self.family)


class PhoneSeen(models.Model):
    family = models.ForeignKey(Family, related_name='phone_no_views')
    seen_at = models.DateTimeField(_('Date and time of number viewed'), auto_now_add=True)
    contact = models.ForeignKey(Family, related_name='contacts')

    class Meta:
        db_table = 'phoneseen'
        verbose_name = _('Phone Seen')
        verbose_name_plural = _('Phone Seen')

    def __str__(self):
        return "%s- %s" % (self.family.father_name, self.family.native_place.name)






# class PhoneShowed(models.Model):
#     bridegroom = models.ForeignKey(BrideGroom, related_name='phone_no_views')



# Phase 2

# class Groom(core_models.Base):
#     pass

    # models.CharField(_('Gothram Name'), max_length=255, choices=(('Gothram', 'Gothram'),))
     # models.CharField(_('Language Name'), max_length=255, choices=(('Tamil', 'Tamil'),))

    # higher_degree = models.CharField(_('Higher Degree'), max_length=255, choices=(('MCA', 'MCA'),))
    # occupations = models.CharField(_('Occupations Name'), max_length=255, choices=(('Software Developer', 'Software Developer'),))

    # raasi = models.CharField(_('Raasi Name'), max_length=255, choices=(('Raasi', 'Raasi'),))
    # religion = models.CharField(_('Religion Name'), max_length=255, choices=(('Hindu', 'Hindu'),))
    # star = models.CharField(_('Stars Name'), max_length=255, choices=(('Stars', 'Stars'),))
