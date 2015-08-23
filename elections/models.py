from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.validators import MinValueValidator
from management.models import Position
from users.models import CustomUser


class Election(models.Model):
    """Model representing an election for staff.

    Attributes:
        - description: string storing the description of the election.
        - end_date: datetime of the end of the election.
        - is_published: boolean indicating if the election is published yet
            meaning users can vote.
        - slug: string only used for SEO.
        - start_date: datetime of the beginning of the election.
        - title: string storing the title of the election.

    Relationships with other models:
        - vacant_positions: several vacant positions associated to this election.

    Ordering by DESCending start_date.

    Clean:
        - start_date cannot be after end_date
    """

    description = models.TextField()
    end_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    slug = models.SlugField()
    start_date = models.DateTimeField()
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('election')
        verbose_name_plural = _('elections')
        ordering = ['-start_date']

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))


class VacantPosition(models.Model):
    """Vacant position of an election.

    A vacant position is a position which is vacant and waiting to be offered to
    members during an election. Current staff for the position which will be
    vacant can be added to the vacant positions and will automatically be elected.
    Maximum number of elected members can be set to anything superior to one to
    enable several members to occupy the same position after election. (Current
    staff added to the vacant position are excluded from this maximum number).

    Attributes:
        - elected_number: integer storing the maximum number of candidates which
            will be elected. (current staff which will stay are excluded).

    Relationships with other models:
        - candidatures: several candidatures associated to this vacant position.
        - election: election associated to this vacant position.
        - position: position which is vacant.
        - staying_staff: several members currently occupying this position and
            automatically re-elected.
    """

    elected_number = models.PositiveSmallIntegerField(default=1,
                        validators=[MinValueValidator(1),])

    election = models.ForeignKey(Election, related_name='vacant_positions',
                limit_choices_to={'end_date__gt': timezone.now})
    position = models.ForeignKey(Position, related_name='vacant_positions')
    staying_staff = models.ManyToManyField(CustomUser,
                    related_name='kept_positions')

    class Meta:
        verbose_name = _('vacant position')
        verbose_name_plural = _('vacant positions')

    # TODO: validate staying_staff in forms
    # http://stackoverflow.com/a/28901357


class Candidature(models.Model):
    """Candidature associated to a vacant position.

    Attributes:
        - speech: string storing the candidature speech of the candidate.

    Relationships with other models:
        - candidate: member who posts this candidature.
        - vacant_position: vacant position associated to this candidature.
        - votes: several votes associated to this candidature.
    """
    speech = models.TextField(blank=True)

    candidate = models.ForeignKey(CustomUser, related_name='candidatures')
    vacant_position = models.ForeignKey(VacantPosition,
                        related_name='candidatures',
                        limit_choices_to={'election__end_date__gt': timezone.now})

    class Meta:
        verbose_name = _('candidature')
        verbose_name_plural = _('candidatures')


class Vote(models.Model):
    """Vote associated to a candidature and a vacant position.

    Members only are allowed to vote in an election. One member can vote for
    one candidate for one vacant position only once.

    Attributes:
        - creation_date: datetime of the creation of the vote. Not editable.

    Relationships with other models:
        - candidature: candidature associated to this vote.
        - voter: member responsible of this vote.

    Clean:
        - the user has to be a member.
        - the user has to not have voted yet for the vacant position associated
            to this candidature.
    """

    creation_date = models.DateTimeField(auto_now_add=True)

    candidature = models.ForeignKey(Candidature, related_name='votes')
    voter = models.ForeignKey(CustomUser, related_name='votes')

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')

    def clean(self):
        if not self.voter.is_member():
            raise ValidationError(_('User currently not a member. Not allowed to \
                                    vote.'))
        if Vote.objects.\
                filter(candidature__vacant_position__candidatures__votes__voter=\
                self.voter).exists():
            raise ValidationError(_('The user already voted for this position.'))
