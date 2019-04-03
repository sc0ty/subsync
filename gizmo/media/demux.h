#ifndef __DEMUX_H__
#define __DEMUX_H__

#include "decoder.h"
#include "stream.h"
#include <vector>
#include <string>
#include <atomic>
#include <memory>

struct AVFormatContext;
struct AVStream;


class Demux
{
	public:
		Demux(const std::string &fileName);
		~Demux();

		Demux(const Demux&) = delete;
		Demux(Demux&&) = delete;
		Demux& operator= (const Demux&) = delete;
		Demux& operator= (Demux&&) = delete;

		const StreamsFormat &getStreamsInfo() const;

		void connectDec(std::shared_ptr<Decoder> dec, unsigned streamId);
		void disconnectDec(std::shared_ptr<Decoder> dec, unsigned streamId);
		void disconnectAllDec(std::shared_ptr<Decoder> dec);

		double getPosition() const;
		double getDuration() const;

		void start();
		void stop();

		bool step();
		void seek(double timestamp);

		void notifyDiscontinuity();
		void flush();

	private:
		AVFormatContext *m_formatContext;
		StreamsFormat m_streamsInfo;
		std::atomic<double> m_position;

	private:
		struct Stream
		{
			typedef std::vector<std::shared_ptr<Decoder>> Decoders;
			Decoders decoders;
			double timeBase;

			Stream();
			void connectDecoder(std::shared_ptr<Decoder> decoder);
			bool disconnectDecoder(std::shared_ptr<Decoder> decoder);
		};

		Stream *m_streams;
		unsigned m_streamsNo;
};

#endif
