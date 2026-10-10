from engine.astro.astro_engine_v3_complete import AstroEngineV3Complete

e = AstroEngineV3Complete()
r = e.full_report('1990-05-04', '21:35', 'Bhandara')
lk = r.get('lal_kitab', {})

print('Total findings:', lk.get('total_findings'))
print('Total remedies:', lk.get('total_remedies'))
print()
print('Planets:')
for f in lk.get('findings', [])[:12]:
    print(f"  {f.get('hindi')} ({f.get('planet')}) - Bhav {f.get('bhav')}")