#ifndef __DEMUX_H__
#define __DEMUX_H__

#include "decoder.h"
#include "stream.h"
#include <vector>
#include <tuple>
#include <string>
#include <atomic>

struct AVFormatContext;
struct AVStream;


class Demux
{
	public:
		Demux(const std::string &fileName);
		~Demux();

		const StreamsFormat &getStreamsInfo() const;

		void connectDec(Decoder *dec, unsigned streamId);
		void disconnectDec(Decoder *dec, unsigned streamId);
		void disconnectAllDec(Decoder *dec);

		double getPosition() const;
		double getDuration() const;

		void start();
		void stop();

		bool step();
		void seek(double timestamp);

		void notifyDiscontinuity();
		void flush();

		AVStream *getStreamRawData(unsigned streamId) const;

		typedef std::tuple<std::string, Decoder*> ConnectedOutput;
		typedef std::vector<ConnectedOutput> ConnectedOutputs;
		ConnectedOutputs getConnectedOutputs() const;

	private:
		AVFormatContext *m_formatContext;
		StreamsFormat m_streamsInfo;
		std::atomic<double> m_position;

	private:
		struct Stream
		{
			typedef std::vector<Decoder*> Decoders;
			Decoders decoders;
			double timeBase;

			Stream();
			void connectDecoder(Decoder *decoder);
			bool disconnectDecoder(Decoder *decoder);
		};

		Stream *m_streams;
		unsigned m_streamsNo;
};

#endif
