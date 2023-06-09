



test= db.session.execute(db.select(Gauge_types,Uncertainties).join(Uncertainties, Gauge_types.id==Uncertainties.gauge_type, isouter=True).order_by(Gauge_types.id)).all()