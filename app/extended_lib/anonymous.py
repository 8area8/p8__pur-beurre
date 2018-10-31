"""Anonymous decorator module.

gist link: https://gist.github.com/m4rc1e/b28cfc9d24c3c2c47f21f2b89cffda86
"""

from django.shortcuts import redirect


def anonymous_required(redirect_url):
    """For views that allow only unauthenticated users to access view.

    Usage:
    @anonymous_required(redirect_url='company_info')
    def homepage(request):
        return render(request, 'homepage.html')
    """
    def _wrapped(view_func, *args, **kwargs):
        def check_anonymous(request, *args, **kwargs):
            view = view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return view
        return check_anonymous
    return _wrapped
